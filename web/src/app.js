/* Louisiana Music Map interface. Reads the embedded data object; all text goes in via textContent. */
(function () {
  'use strict';
  var $ = function (id) { return document.getElementById(id); };
  if (!window.L || !window.LMM) { $('map').textContent = 'The map could not start because its mapping library did not load.'; return; }
  var D = JSON.parse($('lmm-data').textContent);
  var C = window.LMM;

  var genre = {}; D.genres.forEach(function (g) { genre[g.genre_id] = g; });
  var hidden = new Set();            // genre ids switched off in the legend
  var year = D.eras[0].year_start;
  var STEPS = 2000, timer = null, baseName = 'designed';
  var LA = L.latLngBounds([28.85, -94.1], [33.05, -88.8]);

  function el(tag, cls, text) { return C.el(document, tag, cls, text); }
  function css(name) { return getComputedStyle(document.documentElement).getPropertyValue(name).trim(); }
  function span(item) {
    return C.formatYear(item.year_start) + ' – ' + (item.year_end == null ? 'today' : C.formatYear(item.year_end));
  }

  // ---- map and designed basemap -------------------------------------------------------------
  var map = L.map('map', {zoomControl: false, minZoom: 6, maxZoom: 16, maxBounds: LA.pad(0.6), zoomSnap: 0.25});
  L.control.zoom({position: 'bottomleft'}).addTo(map);
  map.attributionControl.setPrefix('');
  // Keep the state clear of the floating legend (left) and era card / panel (right) on wide screens.
  function fitState() {
    var wide = $('stage').clientWidth > 900;
    map.fitBounds(LA, {paddingTopLeft: [wide ? 260 : 8, 8], paddingBottomRight: [wide ? 310 : 8, 8]});
  }
  fitState();
  ['base', 'regions', 'places'].forEach(function (n, i) { map.createPane(n).style.zIndex = 300 + i * 50; });
  map.createPane('labels').style.zIndex = 340;
  map.getPane('labels').style.pointerEvents = 'none';

  var baseLayers = {
    state: L.geoJSON(D.base.state, {pane: 'base', interactive: false}),
    parishes: L.geoJSON(D.base.parishes, {pane: 'base', interactive: false}),
    lakes: L.geoJSON(D.base.lakes, {pane: 'base', interactive: false}),
    rivers: L.geoJSON(D.base.rivers, {pane: 'base', interactive: false})
  };
  var cityLayer = L.layerGroup(D.base.cities.map(function (c) {
    return L.circleMarker([c.lat, c.lon], {pane: 'base', radius: 2, interactive: false, stroke: false, fillOpacity: 0.7})
      .bindTooltip(el('span', null, c.name), {permanent: true, direction: 'right', offset: [4, 0], className: 'city-label', pane: 'labels'});
  }));
  var designed = L.layerGroup([baseLayers.state, baseLayers.lakes, baseLayers.rivers, baseLayers.parishes, cityLayer]);
  function styleBase() {
    baseLayers.state.setStyle({stroke: false, fillColor: css('--land'), fillOpacity: 1});
    baseLayers.parishes.setStyle({fill: false, color: css('--parish'), weight: 0.7});
    baseLayers.lakes.setStyle({stroke: false, fillColor: css('--water'), fillOpacity: 1});
    baseLayers.rivers.setStyle({color: css('--river'), weight: 1.4, fill: false});
    cityLayer.eachLayer(function (m) { m.setStyle({fillColor: css('--muted')}); });
  }
  // Natural regions (EPA Level III ecoregions), shown by the Landscape basemap.
  var ECO_COLORS = {};
  ['34', '35', '65', '73', '74', '75'].forEach(function (id) { ECO_COLORS[id] = css('--eco-' + id); });
  var ecoItems = D.base.ecoregions.features.map(function (f) {
    return {id: 'eco_' + f.properties.eco_id, kind: 'eco', item: f.properties, feature: f, state: 'active'};
  });
  var ecoLayer = L.geoJSON(D.base.ecoregions, {pane: 'base', interactive: false});
  function styleEco() {
    var dark = css('--tiles') === 'dark';
    ecoLayer.setStyle(function (f) {
      return {color: css('--surface'), weight: 1, opacity: 0.9,
              fillColor: ECO_COLORS[f.properties.eco_id] || css('--land'), fillOpacity: dark ? 0.42 : 0.8};
    });
  }
  designed.addTo(map); styleBase(); styleEco();
  if (!ecoItems.length) $('base-landscape').hidden = true;
  function retheme() { styleBase(); styleEco(); render(); if (baseName === 'streets') setBase('streets'); }
  matchMedia('(prefers-color-scheme: dark)').addEventListener('change', retheme);
  new MutationObserver(retheme).observe(document.documentElement, {attributes: true, attributeFilter: ['data-theme']});

  // ---- thematic layers ----------------------------------------------------------------------
  var regions = D.regions.features.map(function (f) {
    var p = f.properties;
    return {id: p.region_id, kind: 'region', item: p, feature: f, state: null,
            layer: L.geoJSON(f, {pane: 'regions', interactive: false})};
  });
  var places = D.places.map(function (p) {
    var m = L.circleMarker([p.lat, p.lon], {pane: 'places', bubblingMouseEvents: true});
    m.bindTooltip(el('span', null, p.name), {direction: 'top', offset: [0, -6]});
    return {id: p.place_id, kind: 'place', item: p, state: null, layer: m};
  });

  var allItems = regions.concat(places).map(function (t) { return t.item; });

  // Places that would overlap on screen merge into one numbered marker. Clicking it zooms in until
  // they separate; at full zoom it lists them instead.
  var CLUSTER_PX = 18, clusterLayer = L.layerGroup().addTo(map), placeById = {};
  places.forEach(function (t) { placeById[t.id] = t; });
  function layoutPlaces() {
    clusterLayer.clearLayers();
    var shown = places.filter(function (t) { return t.state === 'active' || t.state === 'historic'; });
    var pts = shown.map(function (t) {
      var c = map.latLngToContainerPoint(t.layer.getLatLng()); return {id: t.id, x: c.x, y: c.y};
    });
    var inCluster = {};
    C.clusterPoints(pts, CLUSTER_PX).forEach(function (c) {
      if (c.ids.length < 2) return;
      var members = c.ids.map(function (id) { return placeById[id]; });
      members.forEach(function (m) { inCluster[m.id] = true; });
      var faded = members.every(function (m) { return m.state === 'historic'; });
      var icon = L.divIcon({className: 'cluster' + (faded ? ' faded' : ''), html: String(members.length), iconSize: [28, 28]});
      var mk = L.marker(map.containerPointToLatLng([c.x, c.y]),
        {icon: icon, pane: 'places', keyboard: true, title: members.length + ' places here. Select to zoom in.',
         alt: members.length + ' places here'});
      mk.on('click', function () { openCluster(members); });
      clusterLayer.addLayer(mk);
    });
    places.forEach(function (t) {
      t.clustered = !!inCluster[t.id];
      var alone = (t.state === 'active' || t.state === 'historic') && !t.clustered;
      if (alone && !map.hasLayer(t.layer)) t.layer.addTo(map);
      if (!alone && map.hasLayer(t.layer)) map.removeLayer(t.layer);
    });
  }
  function openCluster(members) {
    clearTimeout(clickTimer);
    if (map.getZoom() < map.getMaxZoom() - 0.01) {
      var b = L.latLngBounds(members.map(function (m) { return m.layer.getLatLng(); }));
      map.fitBounds(b.pad(0.6), {maxZoom: map.getMaxZoom()});
    } else {
      chooser(members);
    }
  }
  map.on('zoomend', layoutPlaces);
  function shownState(t) {
    var s = C.stateAt(t.item, year);
    return s === 'future' || C.isHidden(t.item, hidden) ? 'off' : s;
  }
  function render() {
    var ring = css('--surface');
    regions.concat(places).forEach(function (t) {
      var s = shownState(t), color = genre[t.item.genre_id].color, active = s === 'active';
      t.state = s;
      if (t.kind === 'place') {
        if (s !== 'off') {
          t.layer.setStyle({radius: active ? 6.5 : 4, color: ring, weight: 2,
                            opacity: active ? 1 : 0.6, fillColor: color, fillOpacity: active ? 1 : 0.4});
        }
        return;
      }
      if (s === 'off') { if (map.hasLayer(t.layer)) map.removeLayer(t.layer); return; }
      if (!map.hasLayer(t.layer)) t.layer.addTo(map);
      {
        var fill = baseName === 'landscape' ? 0.08 : 0.22;
        t.layer.setStyle({color: color, weight: active ? (baseName === 'landscape' ? 2.4 : 1.8) : 1,
                          opacity: active ? 0.95 : 0.4, dashArray: active ? null : '4 4',
                          fillColor: color, fillOpacity: active ? fill : 0.04});
      }
    });
    layoutPlaces();
    var era = C.eraAt(year, D.eras);
    $('year').textContent = C.formatYear(year);
    $('slider').setAttribute('aria-valuetext', C.formatYear(year) + ', ' + era.name);
    var card = $('era-card');
    if (card.dataset.era !== era.era_id) {
      card.dataset.era = era.era_id;
      var head = el('button', 'era-toggle', era.name); head.type = 'button';
      head.setAttribute('aria-expanded', card.classList.contains('expanded'));
      head.title = 'Show or hide what is happening in this era';
      head.addEventListener('click', function () {
        head.setAttribute('aria-expanded', card.classList.toggle('expanded'));
      });
      var h = el('h2'); h.appendChild(head);
      card.replaceChildren(h, el('p', null, era.summary));
    }
    Array.prototype.forEach.call($('era-ticks').children, function (b) {
      b.classList.toggle('current', b.dataset.era === era.era_id);
    });
    Array.prototype.forEach.call($('legend').querySelectorAll('.row[data-genre]'), function (r) {
      r.classList.toggle('notyet', !C.genreBegun(genre[r.dataset.genre], allItems, year));
      r.classList.toggle('off', hidden.has(r.dataset.genre));
      r.querySelector('.name').setAttribute('aria-pressed', !hidden.has(r.dataset.genre));
    });
  }

  // ---- timeline -----------------------------------------------------------------------------
  function setYear(y, fromSlider) {
    year = y;
    if (!fromSlider) $('slider').value = Math.round(C.yearToFrac(y, D.eras) * STEPS);
    render();
  }
  $('slider').max = STEPS;
  $('slider').addEventListener('input', function () {
    if (!playing) stop();
    setYear(C.fracToYear(this.value / STEPS, D.eras), true);
  });
  D.eras.forEach(function (e) {
    var b = el('button', null, e.name);
    b.type = 'button'; b.dataset.era = e.era_id; b.title = e.name + ' (' + span(e) + ')';
    b.addEventListener('click', function () { stop(); setYear(e.year_start); });
    $('era-ticks').appendChild(b);
  });
  var playing = false;
  function stop() {
    if (timer) { clearInterval(timer); timer = null; }
    $('play').textContent = '▶'; $('play').setAttribute('aria-label', 'Play timeline');
  }
  $('play').addEventListener('click', function () {
    if (timer) return stop();
    if (+$('slider').value >= STEPS) setYear(D.eras[0].year_start);
    this.textContent = '❚❚'; this.setAttribute('aria-label', 'Pause timeline');
    timer = setInterval(function () {
      var v = Math.min(STEPS, +$('slider').value + 3);
      playing = true;                      // setting .value fires no input event, but stay explicit
      $('slider').value = v; setYear(C.fracToYear(v / STEPS, D.eras), true);
      playing = false;
      if (v >= STEPS) stop();
    }, 60);
  });

  // ---- legend -------------------------------------------------------------------------------
  D.genres.slice().sort(function (a, b) { return a.year_start - b.year_start; }).forEach(function (g) {
    var row = el('div', 'row'); row.dataset.genre = g.genre_id;
    var sw = el('span', 'swatch'); sw.style.setProperty('--swatch', g.color); sw.style.background = g.color;
    var name = el('button', 'name', g.name); name.type = 'button'; name.title = 'Show or hide ' + g.name;
    name.addEventListener('click', function () {
      hidden.has(g.genre_id) ? hidden.delete(g.genre_id) : hidden.add(g.genre_id); render();
    });
    var solo = el('button', 'solo', 'only'); solo.type = 'button'; solo.title = 'Show only ' + g.name;
    solo.setAttribute('aria-label', 'Show only ' + g.name + ' and list its regions and places');
    solo.addEventListener('click', function () {
      hidden = new Set(D.genres.map(function (x) { return x.genre_id; })); hidden.delete(g.genre_id);
      stop();
      if (year < g.year_start) setYear(g.year_start); else render();
      openGenre(g);
    });
    row.append(sw, name, solo); $('legend').appendChild(row);
  });
  var all = el('button', 'all', 'Show all genres'); all.type = 'button';
  all.addEventListener('click', function () { hidden.clear(); render(); });
  $('legend').appendChild(all);
  var ecoKey = el('div'); ecoKey.id = 'eco-key'; ecoKey.hidden = true;
  ecoKey.appendChild(el('h3', null, 'Natural regions'));
  ecoItems.forEach(function (t) {
    var row = el('div', 'row'), sw = el('span', 'swatch');
    sw.style.background = ECO_COLORS[t.item.eco_id];
    var name = el('button', 'name', t.item.name); name.type = 'button';
    name.addEventListener('click', function () { openEco(t.item); });
    row.append(sw, name); ecoKey.appendChild(row);
  });
  $('legend').appendChild(ecoKey);
  $('legend-btn').addEventListener('click', function () {
    var open = $('legend').classList.toggle('open'); this.setAttribute('aria-expanded', open);
  });

  // ---- detail panel -------------------------------------------------------------------------
  var returnFocus = null;
  function closePanel() {
    if ($('panel').hidden) return;
    $('panel').hidden = true; $('stage').classList.remove('has-panel');
    // On phones the legend closes when a panel opens, so its buttons cannot take focus back.
    if (returnFocus && returnFocus.offsetParent === null) returnFocus = $('legend-btn');
    if (returnFocus && document.contains(returnFocus)) returnFocus.focus();
    returnFocus = null;
  }
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closePanel(); });
  function panel(nodes) {
    var close = el('button', 'close', '×'); close.type = 'button'; close.setAttribute('aria-label', 'Close');
    close.addEventListener('click', closePanel);
    $('panel').replaceChildren.apply($('panel'), [close].concat(nodes));
    if ($('panel').hidden) returnFocus = document.activeElement;
    $('panel').hidden = false; $('panel').scrollTop = 0;
    if ($('panel').contains(document.activeElement) || (returnFocus && returnFocus !== document.body)) close.focus();
    $('stage').classList.add('has-panel');
    $('legend').classList.remove('open'); $('legend-btn').setAttribute('aria-expanded', false);
  }
  function chips(ids) {
    var wrap = el('div', 'chips');
    ids.forEach(function (id) {
      var c = el('span', 'chip'), dot = el('i'); dot.style.background = genre[id].color;
      c.append(dot, el('span', null, genre[id].name)); wrap.appendChild(c);
    });
    return wrap;
  }
  function links(title, list) {
    if (!list || !list.length) return [];
    var ul = el('ul');
    list.forEach(function (s) {
      var li = el('li'), url = C.safeUrl(s.url);
      if (url) { var a = el('a', null, s.label); a.href = url; a.target = '_blank'; a.rel = 'noopener noreferrer'; li.appendChild(a); }
      else li.textContent = s.label;
      ul.appendChild(li);
    });
    return [el('h3', null, title), ul];
  }
  // "Land and sound": how the physical setting shaped the music, where a source supports it.
  function land(notes) {
    var nodes = [];
    notes.filter(Boolean).forEach(function (n) { nodes.push(el('p', null, n.note)); });
    return nodes.length ? [el('h3', null, 'Land and sound')].concat(nodes) : [];
  }
  function landSources(notes) {
    return notes.filter(Boolean).reduce(function (all, n) { return all.concat(n.sources); }, []);
  }
  function uniqueSources(list) {
    var seen = {};
    return list.filter(function (s) { var k = s.label + '|' + s.url; return seen[k] ? false : (seen[k] = true); });
  }
  // What stands at the spot now. Opens Google Street View; coverage is Google's, so rural sites may show none.
  function streetView(p) {
    var url = C.streetViewUrl(p.lat, p.lon);
    return url ? links('See it today', [{label: 'Street View at this spot (Google Maps)', url: url}]) : [];
  }
  function openPlace(p) {
    var where = [p.town, p.parish ? p.parish + ' Parish' : ''].filter(Boolean).join(', ');
    panel([el('h2', null, p.name), el('div', 'meta', [p.type, where, span(p)].filter(Boolean).join(' · ')),
           chips([p.genre_id].concat(p.other_genres)), el('p', null, p.writeup)]
          .concat(land([p.nature]), links('Listen', p.listen), streetView(p),
                  links('Sources', uniqueSources(p.sources.concat(landSources([p.nature]))))));
  }
  function openRegion(r) {
    var g = genre[r.genre_id], notes = [r.nature, g.nature];
    var nodes = [el('h2', null, r.label), el('div', 'meta', 'Heartland region · ' + span(r)), chips([r.genre_id]),
                 el('p', null, g.summary)];
    if (r.note) nodes.push(el('p', 'meta', r.note));
    panel(nodes.concat(land(notes), links('Sources', uniqueSources(r.sources.concat(g.sources, landSources(notes))))));
  }
  // Every region and place of a genre, as buttons: the keyboard and screen-reader route to each entry.
  function entriesOf(g) {
    var mine = regions.concat(places).filter(function (t) {
      return t.item.genre_id === g.genre_id || (t.item.other_genres || []).indexOf(g.genre_id) >= 0;
    }).sort(function (a, b) { return a.item.year_start - b.item.year_start; });
    if (!mine.length) return [];
    var nodes = [el('h3', null, 'Regions and places')];
    mine.forEach(function (t) {
      var b = el('button', 'choice', (t.kind === 'place' ? t.item.name : t.item.label + ' (region)') + ', ' + span(t.item));
      b.type = 'button'; b.style.borderLeftColor = genre[t.item.genre_id].color;
      b.addEventListener('click', function () {
        if (year < t.item.year_start) setYear(t.item.year_start);
        open(t);
      });
      nodes.push(b);
    });
    return nodes;
  }
  function openGenre(g) {
    panel([el('h2', null, g.name), el('div', 'meta', span(g)), chips([g.genre_id]), el('p', null, g.summary)]
          .concat(land([g.nature]), entriesOf(g),
                  links('Sources', uniqueSources(g.sources.concat(landSources([g.nature]))))));
  }
  function openEco(e) {
    var nodes = [el('h2', null, e.name), el('div', 'meta', 'Natural region · EPA Level III ecoregion ' + e.eco_id)];
    if (e.description) nodes.push(el('p', null, e.description));
    panel(nodes.concat(links('Sources', e.sources)));
  }
  function open(t) { t.kind === 'place' ? openPlace(t.item) : t.kind === 'eco' ? openEco(t.item) : openRegion(t.item); }
  function chooser(hits) {
    var nodes = [el('h2', null, 'Here in ' + C.formatYear(year)), el('div', 'meta', hits.length + ' entries at this spot')];
    // Places before regions, and what is active this year before what has ended.
    var rank = function (t) {
      return (t.kind === 'place' ? 0 : t.kind === 'eco' ? 4 : 2) + (t.state === 'active' ? 0 : 1);
    };
    var heading = {place: 'Places', region: 'Heartland regions', eco: 'Natural region'}, last = null;
    var mixed = hits.some(function (t) { return t.kind !== hits[0].kind; });
    hits.slice().sort(function (a, b) { return rank(a) - rank(b); }).forEach(function (t) {
      if (mixed && t.kind !== last) { nodes.push(el('h3', null, heading[t.kind])); last = t.kind; }
      var label = t.kind === 'place' ? t.item.name
        : t.kind === 'eco' ? t.item.name + ' (natural region)'
        : t.item.label + ' (' + genre[t.item.genre_id].name + ' region)';
      if (t.state === 'historic') label += ', ended ' + C.formatYear(t.item.year_end);
      var b = el('button', 'choice' + (t.state === 'historic' ? ' ended' : ''), label); b.type = 'button';
      b.style.borderLeftColor = t.kind === 'eco' ? ECO_COLORS[t.item.eco_id] : genre[t.item.genre_id].color;
      b.addEventListener('click', function () { open(t); });
      nodes.push(b);
    });
    panel(nodes);
  }
  function hitsAt(containerPoint, latlng) {
    var vis = function (t) { return t.state === 'active' || t.state === 'historic'; };
    var pts = places.filter(function (t) { return vis(t) && !t.clustered; }).map(function (t) {
      var c = map.latLngToContainerPoint(t.layer.getLatLng()); return {id: t.id, x: c.x, y: c.y};
    });
    var ids = C.nearby(pts, containerPoint.x, containerPoint.y, 14);
    var here = [latlng.lng, latlng.lat];
    return ids.map(function (id) { return places.find(function (t) { return t.id === id; }); })
      .concat(regions.filter(function (t) { return vis(t) && C.pointInFeature(here, t.feature); }))
      .concat(baseName === 'landscape' ? ecoItems.filter(function (t) { return C.pointInFeature(here, t.feature); }) : []);
  }
  var clickTimer = null;
  map.on('click', function (e) {
    clearTimeout(clickTimer);
    clickTimer = setTimeout(function () {
      var hits = hitsAt(e.containerPoint, e.latlng);
      if (!hits.length) { closePanel(); return; }
      hits.length === 1 ? open(hits[0]) : chooser(hits);
    }, 230);
  });
  map.on('dblclick', function () { clearTimeout(clickTimer); });

  // ---- online basemaps with fallback --------------------------------------------------------
  var TILES = {
    streets: function () {
      var style = css('--tiles') === 'dark' ? 'dark_all' : 'light_all';
      return L.tileLayer('https://{s}.basemaps.cartocdn.com/' + style + '/{z}/{x}/{y}{r}.png',
        {subdomains: 'abcd', maxZoom: 19, attribution: '© OpenStreetMap contributors © CARTO'});
    },
    satellite: function () {
      return L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        {maxZoom: 19, attribution: 'Imagery © Esri, Maxar, Earthstar Geographics'});
    }
  };
  var tileLayer = null, noticeTimer = null;
  function notice(text) {
    $('notice').textContent = text; $('notice').hidden = false;
    clearTimeout(noticeTimer); noticeTimer = setTimeout(function () { $('notice').hidden = true; }, 5000);
  }
  function setBase(name) {
    if (tileLayer) { map.removeLayer(tileLayer); tileLayer = null; }
    baseName = name;
    var builtIn = name === 'designed' || name === 'landscape';
    if (name === 'landscape') { ecoLayer.addTo(map); } else { map.removeLayer(ecoLayer); }
    $('eco-key').hidden = name !== 'landscape';
    if (builtIn) {
      designed.addTo(map); map.setMaxZoom(16);
      if (name === 'landscape') { ecoLayer.bringToBack(); baseLayers.state.bringToBack(); }
    } else {
      var loaded = 0, failed = 0;
      tileLayer = TILES[name]().addTo(map);
      tileLayer.on('tileload', function () { loaded++; });
      tileLayer.on('tileerror', function () {
        if (++failed >= 4 && loaded === 0 && baseName === name) {
          notice('Online basemap unavailable. Showing the built-in map.'); setBase('designed');
        }
      });
      map.removeLayer(designed); map.setMaxZoom(18);
    }
    Array.prototype.forEach.call($('basemaps').children, function (b) {
      b.setAttribute('aria-pressed', b.dataset.base === name);
    });
    render();
  }
  Array.prototype.forEach.call($('basemaps').children, function (b) {
    b.addEventListener('click', function () { setBase(b.dataset.base); });
  });
  // Offer the online basemaps only if a tile can actually be fetched from here.
  var probe = new Image();
  probe.onload = function () { $('base-streets').hidden = false; $('base-satellite').hidden = false; };
  probe.src = 'https://a.basemaps.cartocdn.com/light_all/6/15/26.png';

  // ---- about --------------------------------------------------------------------------------
  (function () {
    var d = $('about'), c = D.meta.counts, close = el('button', null, 'Close'); close.type = 'button';
    close.addEventListener('click', function () { d.close(); });
    d.append(
      el('h2', null, 'About this map'),
      el('p', null, c.places + ' places and ' + c.regions + ' heartland regions across ' + c.genres +
        ' genres and traditions. Built ' + D.meta.built + '.'),
      el('p', null, 'Heartland regions are approximations drawn from groups of parishes. Music does not stop at a parish line; the shapes show where a tradition was centered, not where it was confined.'),
      el('p', null, 'For the ancient period there are no recordings and little direct evidence of music. Entries there state what archaeology and tribal nations’ own accounts support, and say so where something is inferred.'),
      el('p', null, 'Colors help tell genres apart, but with this many they cannot do it alone. Hover or tap anything for its name, or use “only” in the genre list to isolate one.'),
      el('p', null, 'Boundaries: U.S. Census Bureau. Rivers and lakes: Natural Earth. Natural regions: U.S. EPA Level III ecoregions. Online basemaps: OpenStreetMap contributors, CARTO, Esri. Mapping library: Leaflet.'),
      close);
    $('about-btn').addEventListener('click', function () { d.showModal(); });
  })();

  window.LMMApp = {
    setYear: function (y) { stop(); setYear(y); },
    getYear: function () { return year; },
    layout: function () {
      return {zoom: map.getZoom(), clusters: clusterLayer.getLayers().length,
              clustered: places.filter(function (t) { return t.clustered; }).length,
              alone: places.filter(function (t) { return map.hasLayer(t.layer); }).length};
    },
    zoomTo: function (lat, lng, z) { map.setView([lat, lng], z, {animate: false}); return map.getZoom(); },
    openFirstCluster: function () { var l = clusterLayer.getLayers()[0]; if (l) l.fire('click'); return !!l; },
    setBase: function (name) { setBase(name); return baseName; },
    visibleCounts: function () {
      var n = function (list) { return list.filter(function (t) { return t.state !== 'off'; }).length; };
      return {regions: n(regions), places: n(places)};
    },
    hitsAtLatLng: function (lat, lng) {
      var ll = L.latLng(lat, lng);
      return hitsAt(map.latLngToContainerPoint(ll), ll).map(function (t) { return t.id; });
    }
  };
  setYear(year);
  requestAnimationFrame(function () { map.invalidateSize(); fitState(); });
})();
