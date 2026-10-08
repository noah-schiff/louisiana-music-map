/* Pure functions for the timeline and hit-testing. No DOM, no Leaflet. */
(function (root) {
  'use strict';

  function clamp(v, lo, hi) { return Math.max(lo, Math.min(hi, v)); }

  function yearToFrac(year, eras) {
    var n = eras.length;
    year = clamp(year, eras[0].year_start, eras[n - 1].year_end);
    for (var i = 0; i < n; i++) {
      var e = eras[i];
      if (year <= e.year_end) return (i + (year - e.year_start) / (e.year_end - e.year_start)) / n;
    }
    return 1;
  }

  function fracToYear(frac, eras) {
    var n = eras.length;
    frac = clamp(frac, 0, 1);
    var i = Math.min(n - 1, Math.floor(frac * n));
    var e = eras[i];
    var y = Math.round(e.year_start + (frac * n - i) * (e.year_end - e.year_start));
    return y === 0 ? 1 : y;
  }

  function eraAt(year, eras) {
    for (var i = 0; i < eras.length; i++) if (year < eras[i].year_end) return eras[i];
    return eras[eras.length - 1];
  }

  function stateAt(item, year) {
    if (year < item.year_start) return 'future';
    if (item.year_end == null || year <= item.year_end) return 'active';
    return 'historic';
  }

  function formatYear(y) {
    if (y < 0) return (-y) + ' BCE';
    return y < 1000 ? y + ' CE' : String(y);
  }

  function nearby(points, x, y, radius) {
    return points
      .map(function (p) { return {id: p.id, d: Math.hypot(p.x - x, p.y - y)}; })
      .filter(function (p) { return p.d <= radius; })
      .sort(function (a, b) { return a.d - b.d || (a.id < b.id ? -1 : a.id > b.id ? 1 : 0); })
      .map(function (p) { return p.id; });
  }

  function inRing(pt, ring) {
    var x = pt[0], y = pt[1], inside = false;
    for (var i = 0, j = ring.length - 1; i < ring.length; j = i++) {
      var xi = ring[i][0], yi = ring[i][1], xj = ring[j][0], yj = ring[j][1];
      if ((yi > y) !== (yj > y) && x < (xj - xi) * (y - yi) / (yj - yi) + xi) inside = !inside;
    }
    return inside;
  }

  function inPolygon(pt, rings) {
    if (!inRing(pt, rings[0])) return false;
    for (var k = 1; k < rings.length; k++) if (inRing(pt, rings[k])) return false;
    return true;
  }

  function pointInFeature(pt, feature) {
    var g = feature.geometry;
    if (g.type === 'Polygon') return inPolygon(pt, g.coordinates);
    if (g.type === 'MultiPolygon') return g.coordinates.some(function (rings) { return inPolygon(pt, rings); });
    return false;
  }

  function safeUrl(url) { return /^https?:\/\//i.test(url || '') ? url : ''; }

  // Build an element whose text is always literal. Research text goes through here, never innerHTML.
  function el(doc, tag, cls, text) {
    var n = doc.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }

  // A genre has "begun" once its own start year arrives or any of its entries is already on the map
  // (a hall can predate the music it later became known for).
  function genreBegun(genre, items, year) {
    if (year >= genre.year_start) return true;
    return items.some(function (i) { return i.genre_id === genre.genre_id && stateAt(i, year) !== 'future'; });
  }

  // An entry is hidden only when every genre it belongs to is switched off in the legend.
  function isHidden(item, hiddenSet) {
    return [item.genre_id].concat(item.other_genres || []).every(function (g) { return hiddenSet.has(g); });
  }

  // Google's keyless Maps URL for a Street View panorama at a point; '' if the point is not usable.
  function streetViewUrl(lat, lon) {
    if (typeof lat !== 'number' || typeof lon !== 'number' || !isFinite(lat) || !isFinite(lon)) return '';
    if (Math.abs(lat) > 90 || Math.abs(lon) > 180) return '';
    return 'https://www.google.com/maps/@?api=1&map_action=pano&viewpoint=' + encodeURIComponent(lat + ',' + lon);
  }

  root.LMM = {el: el, genreBegun: genreBegun, isHidden: isHidden, streetViewUrl: streetViewUrl, yearToFrac: yearToFrac, fracToYear: fracToYear, eraAt: eraAt, stateAt: stateAt,
              formatYear: formatYear, nearby: nearby, pointInFeature: pointInFeature, safeUrl: safeUrl};
})(window);
