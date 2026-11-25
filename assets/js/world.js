/* The Yatra Express: a 3D train journey, one gesture per stop. Needs three.js (bundled). Falls back to the text version. */
(function () {
  'use strict';
  var D = window.YATRA, N = D.chapters.length, root = document.documentElement;
  function $(id) { return document.getElementById(id); }
  function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }
  function lerp(a, b, t) { return a + (b - a) * t; }
  function smooth(a, b, x) { var t = clamp((x - a) / (b - a), 0, 1); return t * t * (3 - 2 * t); }
  function store(k, v) { try { if (v === undefined) return window.localStorage.getItem(k); window.localStorage.setItem(k, v); } catch (e) { return null; } }
  var reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  /* quality tier: phones and touch devices get a lighter world; a frame-rate governor lowers it further if needed */
  var LOW = window.innerWidth < 760 || (window.matchMedia && window.matchMedia('(pointer:coarse)').matches), DEN = LOW ? .55 : 1;
  var prCap = LOW ? 1.25 : 1.75, qLevel = 0, frameN = 0, fsum = 0;

  /* ---------- 3D, or the stacked fallback when WebGL is unavailable ---------- */
  try { if ('scrollRestoration' in history) history.scrollRestoration = 'manual'; } catch (e) {}
  var renderer = null, running = false, started = false, plainEl = $('plain');
  function setPlain(on) {
    root.classList.toggle('plain-on', on); plainEl.hidden = !on;
    if (on) { running = false; }
    else if (renderer) { running = true; if (!started) start(); window.requestAnimationFrame(frame); }
  }
  try {
    if (window.THREE) renderer = new THREE.WebGLRenderer({ canvas: $('gl'), antialias: window.devicePixelRatio < 2 && !LOW, powerPreference: 'high-performance' });
  } catch (e) { renderer = null; }
  if (!renderer) { root.classList.add('plain-on'); return; }
  var initialPlain = false;
  $('hud').hidden = false;

  /* ---------- constants ---------- */
  var SP = 130, Z0 = -20, LAST = Z0 - (N - 1) * SP, LANES = [0];
  var RIVERS = [Z0 - SP * 2.5, Z0 - SP * 5.5, Z0 - SP * 7.5], CROSS = [Z0 - SP * 1.5, Z0 - SP * 3.5, Z0 - SP * 6.5, Z0 - SP * 7.9];
  var LEN = (Z0 + 220) - (LAST - 320), ZC = ((Z0 + 220) + (LAST - 320)) / 2;
  function zStation(i) { return Z0 - i * SP; }
  function rng(seed) { return function () { seed |= 0; seed = seed + 0x6D2B79F5 | 0; var t = Math.imul(seed ^ seed >>> 15, 1 | seed); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; };
  var R = rng(20261117);

  /* ---------- biome table: one entry per chapter, interpolated along the track ---------- */
  function H(x) { return new THREE.Color(x); }
  var B_all = [
    /* 0 telangana dawn   */ { top: 0x24356b, hor: 0xffb06a, g1: 0x6f9a45, g2: 0x9db856, sunY: .10, sunC: 0xffc27a, sunI: .9, hemi: .55, star: .5, amp: 4, fogN: 60, fogF: 420, tree: .7, build: 0, hut: .4, mount: 0, cactus: 0, leaf: 0x3f7a35, glow: 1 },
    /* 1 cairo dusk       */ { top: 0x3a2a5a, hor: 0xff8a5b, g1: 0xc9a15f, g2: 0xe2bd7a, sunY: .06, sunC: 0xff9a5a, sunI: .8, hemi: .5, star: .55, amp: 7, fogN: 60, fogF: 380, tree: .06, build: .12, hut: .1, mount: 0, cactus: .3, leaf: 0x6e8a3a, glow: 1 },
    /* 2 narayanpet day   */ { top: 0x3f86d6, hor: 0xcfe8ff, g1: 0x86ad45, g2: 0xb2c25e, sunY: .75, sunC: 0xfff3d0, sunI: 1.15, hemi: .8, star: 0, amp: 4, fogN: 80, fogF: 520, tree: .6, build: .05, hut: .6, mount: 0, cactus: 0, leaf: 0x3f8a3a, glow: 0 },
    /* 3 jagriti golden   */ { top: 0x3b66b0, hor: 0xffd7a0, g1: 0x9bb355, g2: 0xc9b860, sunY: .28, sunC: 0xffd08a, sunI: 1.05, hemi: .7, star: 0, amp: 5, fogN: 70, fogF: 460, tree: .45, build: .08, hut: .5, mount: 0, cactus: .05, leaf: 0x5a8a3a, glow: .4 },
    /* 4 ahmedabad bright */ { top: 0x3a8fe0, hor: 0xe3f1ff, g1: 0xb3aa5c, g2: 0xd2c47a, sunY: .8, sunC: 0xffffff, sunI: 1.2, hemi: .85, star: 0, amp: 3, fogN: 90, fogF: 560, tree: .3, build: .6, hut: .3, mount: 0, cactus: .1, leaf: 0x6f9a3a, glow: 0 },
    /* 5 nagaland mist    */ { top: 0x4a6a86, hor: 0xcfe0dc, g1: 0x3f7a55, g2: 0x5f9a68, sunY: .5, sunC: 0xeaf3e8, sunI: .85, hemi: .75, star: 0, amp: 22, fogN: 40, fogF: 230, tree: 1, build: 0, hut: .25, mount: 1, cactus: 0, leaf: 0x2a6a40, glow: .2 },
    /* 6 nagaur desert    */ { top: 0x3a86d6, hor: 0xffe4b4, g1: 0xd9a35c, g2: 0xeac27c, sunY: .85, sunC: 0xfff0c8, sunI: 1.3, hemi: .85, star: 0, amp: 9, fogN: 80, fogF: 520, tree: .04, build: 0, hut: .15, mount: .1, cactus: .5, leaf: 0x7a8a3a, glow: 0 },
    /* 7 delhi haze       */ { top: 0x6b86a8, hor: 0xd9d2c4, g1: 0x8a9a7a, g2: 0xa6b08a, sunY: .55, sunC: 0xfff0d8, sunI: .95, hemi: .75, star: 0, amp: 3, fogN: 50, fogF: 330, tree: .4, build: .85, hut: .1, mount: 0, cactus: 0, leaf: 0x4f7a3a, glow: .3 },
    /* 8 gandhinagar eve  */ { top: 0x2d3a7a, hor: 0xff9f6b, g1: 0x7aa05a, g2: 0xa2b66a, sunY: .12, sunC: 0xff9a60, sunI: .85, hemi: .55, star: .35, amp: 5, fogN: 60, fogF: 420, tree: .5, build: .3, hut: .2, mount: 0, cactus: .05, leaf: 0x4f8a3a, glow: .9 },
    /* 9 boston autumn    */ { top: 0x0b1230, hor: 0x35457a, g1: 0x8a4a2a, g2: 0xb5651d, sunY: -.2, sunC: 0x8fa6ff, sunI: .4, hemi: .45, star: 1, amp: 8, fogN: 50, fogF: 330, tree: .95, build: .15, hut: 0, mount: 0, cactus: 0, leaf: 0xd5681d, glow: 1 },
    /* 10 gurugram dusk   */ { top: 0x121c42, hor: 0xe0795a, g1: 0x587a5a, g2: 0x7a9a68, sunY: .04, sunC: 0xff8a5a, sunI: .7, hemi: .5, star: .7, amp: 4, fogN: 60, fogF: 400, tree: .4, build: 1, hut: 0, mount: 0, cactus: 0, leaf: 0x3f7a4a, glow: 1 },
    /* 11 you, sunrise    */ { top: 0x1b2a5c, hor: 0xffb36b, g1: 0x6f9a52, g2: 0x9cbc62, sunY: .14, sunC: 0xffc88a, sunI: 1, hemi: .6, star: .3, amp: 4, fogN: 70, fogF: 480, tree: .6, build: .1, hut: .3, mount: 0, cactus: 0, leaf: 0x4f9a3a, glow: .7 }
  ];
  var B = D.chapters.map(function (c) { return B_all[c.biome]; });
  while (B.length < N) B.push(B[B.length - 1]);
  var NUM = ['sunY', 'sunI', 'hemi', 'star', 'amp', 'fogN', 'fogF', 'tree', 'build', 'hut', 'mount', 'cactus', 'glow'], COL = ['top', 'hor', 'g1', 'g2', 'sunC', 'leaf'];
  var tmpA = new THREE.Color(), tmpB = new THREE.Color();
  var bioOut = {}; COL.forEach(function (k) { bioOut[k] = new THREE.Color(); });
  function bio(fv) {
    fv = clamp(fv, 0, N - 1.0001);
    var i = Math.floor(fv), t = fv - i, a = B[i], b = B[i + 1], o = bioOut;
    NUM.forEach(function (k) { o[k] = lerp(a[k], b[k], t); });
    COL.forEach(function (k) { o[k].set(a[k]).lerp(tmpB.set(b[k]), t); });
    return o;
  }
  function fvAtZ(z) { return clamp((Z0 - z) / SP, 0, N - 1); }

  /* ---------- scene ---------- */
  renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  var scene = new THREE.Scene(), camera = new THREE.PerspectiveCamera(62, 1, .5, 1400);
  scene.fog = new THREE.Fog(0x88aacc, 60, 420);
  var hemi = new THREE.HemisphereLight(0xffffff, 0x445533, .7); scene.add(hemi);
  var sun = new THREE.DirectionalLight(0xffffff, 1); sun.castShadow = true; var SM = LOW ? 512 : 1536; sun.shadow.mapSize.set(SM, SM); var sc0 = sun.shadow.camera; var shR = LOW ? 38 : 48; sc0.left = -shR; sc0.right = shR; sc0.top = shR; sc0.bottom = -shR; sc0.near = 1; sc0.far = 320; sun.shadow.bias = -.0006; sun.shadow.normalBias = .4; scene.add(sun); scene.add(sun.target);

  var sky = new THREE.Mesh(new THREE.SphereGeometry(900, 24, 16), new THREE.ShaderMaterial({
    side: THREE.BackSide, depthWrite: false, fog: false,
    uniforms: { top: { value: new THREE.Color() }, hor: { value: new THREE.Color() }, sunDir: { value: new THREE.Vector3(0, 1, 0) }, sunC: { value: new THREE.Color() } },
    vertexShader: 'varying vec3 vP;void main(){vP=position;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}',
    fragmentShader: 'uniform vec3 top;uniform vec3 hor;uniform vec3 sunDir;uniform vec3 sunC;varying vec3 vP;void main(){vec3 d=normalize(vP);float h=d.y;vec3 c=mix(hor,top,smoothstep(0.,.7,h));if(h<0.)c=hor*.85;c+=sunC*pow(max(dot(d,normalize(sunDir)),0.),22.)*.9;gl_FragColor=vec4(c,1.);}'
  }));
  sky.renderOrder = -2; scene.add(sky);
  var sunMesh = new THREE.Mesh(new THREE.SphereGeometry(26, 20, 14), new THREE.MeshBasicMaterial({ color: 0xffd9a0, fog: false })); scene.add(sunMesh);
  var starGeo = new THREE.BufferGeometry(), sp = [];
  for (var s = 0; s < (LOW ? 350 : 700); s++) { var th = R() * 6.283, ph = Math.acos(R() * .95 + .02), rr = 850; sp.push(rr * Math.sin(ph) * Math.cos(th), rr * Math.cos(ph), rr * Math.sin(ph) * Math.sin(th)); }
  starGeo.setAttribute('position', new THREE.Float32BufferAttribute(sp, 3));
  var stars = new THREE.Points(starGeo, new THREE.PointsMaterial({ color: 0xffffff, size: 2.4, sizeAttenuation: false, transparent: true, opacity: 0, fog: false, depthWrite: false })); scene.add(stars);

  /* ---------- terrain ---------- */
  function noise(x, z) { return .5 * Math.sin(x * .045 + Math.sin(z * .021) * 2.1) * Math.cos(z * .037 + x * .01) + .3 * Math.sin(x * .11 + z * .083) + .2 * Math.sin(z * .19 + x * .07); }
  function hAt(x, z) { var b = biomeAmp(z), m = smooth(15, 62, Math.abs(x)), rv = 1; for (var ri = 0; ri < RIVERS.length; ri++) rv = Math.min(rv, smooth(13, 26, Math.abs(z - RIVERS[ri]))); return (noise(x, z) * .5 + .5) * b * m * rv; }
  function biomeAmp(z) { var fv = clamp(fvAtZ(z), 0, N - 1.0001), i = Math.floor(fv), t = fv - i; return lerp(B[i].amp, B[i + 1].amp, t); }
  var tg = new THREE.PlaneGeometry(380, LEN, LOW ? 52 : 76, LOW ? 230 : 380); tg.rotateX(-Math.PI / 2);
  var tp = tg.attributes.position, tc = new Float32Array(tp.count * 3), c1 = new THREE.Color(), c2 = new THREE.Color(), cc = new THREE.Color();
  for (var v = 0; v < tp.count; v++) {
    var vx = tp.getX(v), vz = tp.getZ(v) + ZC, hh = hAt(vx, vz); tp.setY(v, hh); tp.setZ(v, vz);
    var fvv = clamp(fvAtZ(vz), 0, N - 1.0001), ii = Math.floor(fvv), tt = fvv - ii;
    c1.set(B[ii].g1).lerp(tmpB.set(B[ii + 1].g1), tt); c2.set(B[ii].g2).lerp(tmpB.set(B[ii + 1].g2), tt);
    cc.copy(c1).lerp(c2, clamp(noise(vx * 1.7, vz * 1.3) * .5 + .5, 0, 1)).multiplyScalar(.82 + hh * .012);
    tc[v * 3] = cc.r; tc[v * 3 + 1] = cc.g; tc[v * 3 + 2] = cc.b;
  }
  tg.setAttribute('color', new THREE.BufferAttribute(tc, 3)); tg.computeVertexNormals();
  var terrain = new THREE.Mesh(tg, new THREE.MeshStandardMaterial({ vertexColors: true, flatShading: true, roughness: 1 })); terrain.receiveShadow = true; scene.add(terrain);

  /* ---------- track ---------- */
  var bed = new THREE.Mesh(new THREE.BoxGeometry(15, .14, LEN), new THREE.MeshStandardMaterial({ color: 0x6d655c, roughness: 1 })); bed.position.set(0, .05, ZC); bed.receiveShadow = true; scene.add(bed);
  var railMat = new THREE.MeshStandardMaterial({ color: 0xc8ccd2, metalness: .7, roughness: .4 });
  LANES.forEach(function (lx) { [-.72, .72].forEach(function (o) { var r = new THREE.Mesh(new THREE.BoxGeometry(.12, .16, LEN), railMat); r.position.set(lx + o, .22, ZC); scene.add(r); }); });
  var nSl = Math.floor(LEN / 1.25), sl = new THREE.InstancedMesh(new THREE.BoxGeometry(2.3, .12, .48), new THREE.MeshStandardMaterial({ color: 0x4a3a2c, roughness: 1 }), nSl * LANES.length), dm = new THREE.Object3D(), si = 0;
  for (var l = 0; l < LANES.length; l++) for (var k = 0; k < nSl; k++) { dm.position.set(LANES[l], .16, ZC + LEN / 2 - k * 1.25); dm.updateMatrix(); sl.setMatrixAt(si++, dm.matrix); }
  scene.add(sl);

  /* ---------- draw-call savers: merge static meshes ---------- */
  function isDyn(o) { while (o) { if (o.userData && o.userData.dyn) return true; o = o.parent; } return false; }
  function mergeMeshes(root, list, mat, useColor) {
    if (!list.length) return null;
    root.updateMatrixWorld(true); var inv = new THREE.Matrix4().copy(root.matrixWorld).invert(), M = new THREE.Matrix4(), nm = new THREE.Matrix3(), v = new THREE.Vector3(), P = [], Nn = [], Cc = [];
    list.forEach(function (o) {
      var g = o.geometry.index ? o.geometry.toNonIndexed() : o.geometry, pos = g.attributes.position, nor = g.attributes.normal; M.multiplyMatrices(inv, o.matrixWorld); nm.getNormalMatrix(M);
      for (var i = 0; i < pos.count; i++) { v.fromBufferAttribute(pos, i).applyMatrix4(M); P.push(v.x, v.y, v.z); v.fromBufferAttribute(nor, i).applyMatrix3(nm).normalize(); Nn.push(v.x, v.y, v.z); if (useColor) Cc.push(o.material.color.r, o.material.color.g, o.material.color.b); }
      if (o.parent) o.parent.remove(o);
    });
    var geo = new THREE.BufferGeometry(); geo.setAttribute('position', new THREE.Float32BufferAttribute(P, 3)); geo.setAttribute('normal', new THREE.Float32BufferAttribute(Nn, 3)); if (useColor) geo.setAttribute('color', new THREE.Float32BufferAttribute(Cc, 3));
    var mesh = new THREE.Mesh(geo, mat); root.add(mesh); return mesh;
  }
  var sharedFlat = new THREE.MeshStandardMaterial({ vertexColors: true, flatShading: true, roughness: 1 }), mergedBuckets = [];
  function consolidateWorld() {
    scene.updateMatrixWorld(true); var buckets = {}, dead = [], v = new THREE.Vector3(), nm = new THREE.Matrix3();
    scene.traverse(function (o) {
      if (!o.isMesh || o.isInstancedMesh || o === terrain || o === bed) return; var m = o.material;
      if (!m || Array.isArray(m) || !m.isMeshStandardMaterial || m.map || m.transparent || m.vertexColors || (m.userData && m.userData.lit) || m.metalness > .3 || isDyn(o)) return;
      var g = o.geometry.index ? o.geometry.toNonIndexed() : o.geometry, pos = g.attributes.position, nor = g.attributes.normal, key = Math.floor(-o.matrixWorld.elements[14] / 160), bk = buckets[key] || (buckets[key] = { P: [], N: [], C: [] });
      nm.getNormalMatrix(o.matrixWorld);
      for (var i = 0; i < pos.count; i++) { v.fromBufferAttribute(pos, i).applyMatrix4(o.matrixWorld); bk.P.push(v.x, v.y, v.z); v.fromBufferAttribute(nor, i).applyMatrix3(nm).normalize(); bk.N.push(v.x, v.y, v.z); bk.C.push(m.color.r, m.color.g, m.color.b); }
      dead.push(o);
    });
    dead.forEach(function (o) { if (o.parent) o.parent.remove(o); });
    Object.keys(buckets).forEach(function (k) { var bk = buckets[k], geo = new THREE.BufferGeometry(); geo.setAttribute('position', new THREE.Float32BufferAttribute(bk.P, 3)); geo.setAttribute('normal', new THREE.Float32BufferAttribute(bk.N, 3)); geo.setAttribute('color', new THREE.Float32BufferAttribute(bk.C, 3)); var mesh = new THREE.Mesh(geo, sharedFlat); mesh.castShadow = !LOW; mesh.receiveShadow = true; mesh.userData.zc = -(Number(k) * 160 + 80); scene.add(mesh); mergedBuckets.push(mesh); });
  }

  /* ---------- lit windows: a world-space window grid that glows at dusk ---------- */
  var litShaders = [];
  function litMaterial(hex) {
    var m = new THREE.MeshStandardMaterial({ color: hex, flatShading: true, roughness: .8 });
    m.onBeforeCompile = function (sh) {
      sh.uniforms.uGlow = { value: 0 }; litShaders.push(sh);
      sh.vertexShader = sh.vertexShader.replace('#include <common>', '#include <common>\nvarying vec3 vW;')
        .replace('#include <begin_vertex>', '#include <begin_vertex>\nvec4 wp = vec4(transformed, 1.0);\n#ifdef USE_INSTANCING\nwp = instanceMatrix * wp;\n#endif\nwp = modelMatrix * wp; vW = wp.xyz;');
      sh.fragmentShader = sh.fragmentShader.replace('#include <common>', '#include <common>\nvarying vec3 vW; uniform float uGlow;')
        .replace('#include <emissivemap_fragment>', '#include <emissivemap_fragment>\nvec2 gq = vec2(vW.x + vW.z, vW.y) / vec2(3.0, 3.6); vec2 gf = fract(gq); float win = step(.25, gf.x) * step(gf.x, .75) * step(.3, gf.y) * step(gf.y, .72); float rr = fract(sin(dot(floor(gq), vec2(12.9, 78.2))) * 43758.5); totalEmissiveRadiance += vec3(1., .78, .42) * win * step(.42, rr) * uGlow * 1.6;');
    };
    return m;
  }

  /* ---------- props (instanced) ---------- */
  function placeMesh(geo, mat, items, colorFn) {
    if (!items.length) return;
    var im = new THREE.InstancedMesh(geo, mat, items.length), o = new THREE.Object3D(), col = new THREE.Color();
    items.forEach(function (it, i) { o.position.set(it.x, it.y, it.z); o.rotation.set(0, it.ry || 0, 0); o.scale.set(it.sx, it.sy, it.sz); o.updateMatrix(); im.setMatrixAt(i, o.matrix); if (colorFn) { colorFn(col, it); im.setColorAt(i, col); } });
    im.castShadow = !LOW; im.receiveShadow = !LOW; scene.add(im);
  }
  var cone = new THREE.ConeGeometry(2.1, 6, 6); cone.translate(0, 5, 0);
  var trunk = new THREE.CylinderGeometry(.3, .45, 2.2, 5); trunk.translate(0, 1.1, 0);
  var boxG = new THREE.BoxGeometry(1, 1, 1); boxG.translate(0, .5, 0);
  var roofG = new THREE.ConeGeometry(.9, .8, 4); roofG.translate(0, 1.2, 0); roofG.rotateY(Math.PI / 4);
  var mountG = new THREE.ConeGeometry(1, 1, 5); mountG.translate(0, .5, 0);
  var cactusG = new THREE.CylinderGeometry(.35, .45, 3.2, 6); cactusG.translate(0, 1.6, 0);
  var trees = [], trunks = [], huts = [], roofs = [], blds = [], mounts = [], cacti = [], poles = [];
  var zmin = LAST - 260, zmax = Z0 + 140;
  for (var z = zmax; z > zmin; z -= 5) {
    var fv = fvAtZ(z), b = bio(fv);
    for (var sd = -1; sd <= 1; sd += 2) {
      if (R() < b.tree * .55 * DEN) { var tx = sd * (16 + R() * 90), ty = hAt(tx, z), sc = .8 + R() * 1.1; trees.push({ x: tx, y: ty, z: z + R() * 5, sx: sc, sy: sc * (.9 + R() * .5), sz: sc, c: b.leaf.clone().multiplyScalar(.8 + R() * .4) }); trunks.push({ x: tx, y: ty, z: z, sx: sc, sy: sc, sz: sc }); }
      if (R() < b.hut * .07 * DEN) { var hx = sd * (14 + R() * 26), hy = hAt(hx, z), w = 3 + R() * 2.4; huts.push({ x: hx, y: hy, z: z, sx: w, sy: 2.4, sz: w * 1.2, ry: R() * 1.5, c: new THREE.Color(0xd9c7a8).multiplyScalar(.8 + R() * .3) }); roofs.push({ x: hx, y: hy + 2.4, z: z, sx: w * 1.5, sy: 1.5, sz: w * 1.7, ry: 0, c: new THREE.Color(0xb5503a) }); }
      if (R() < b.build * .1 * DEN) { var bx = sd * (20 + R() * 55), bw = 6 + R() * 10, bh = 8 + R() * 34 * (b.build > .7 ? 1.5 : 1); blds.push({ x: bx, y: hAt(bx, z), z: z, sx: bw, sy: bh, sz: bw, c: new THREE.Color().setHSL(.58 + R() * .05, .12 + R() * .1, .42 + R() * .25) }); }
      if (R() < b.cactus * .08 * DEN) { var cx = sd * (14 + R() * 60); cacti.push({ x: cx, y: hAt(cx, z), z: z, sx: .8 + R() * .8, sy: .8 + R() * 1.2, sz: .8 + R() * .8 }); }
    }
  }
  for (var zm = zmax + 40; zm > zmin - 100; zm -= 34) {
    var bm = bio(fvAtZ(zm));
    for (var sm = -1; sm <= 1; sm += 2) if (R() < bm.mount * .85 + .06) { var mw = 50 + R() * 90, mh = 40 + R() * 90 * (bm.mount + .3); mounts.push({ x: sm * (95 + R() * 120), y: -3, z: zm, sx: mw, sy: mh, sz: mw, ry: R() * 3, c: new THREE.Color().lerpColors(new THREE.Color(0x5b7a8a), bm.hor, .25 + .45 * R()) }); }
  }
  for (var zp = zmax; zp > zmin; zp -= 26) [-1, 1].forEach(function (sd2) { poles.push({ x: sd2 * 9.4, y: 0, z: zp, sx: .25, sy: 8, sz: .25 }); });
  var flat = function (hex) { return new THREE.MeshStandardMaterial({ color: hex, flatShading: true, roughness: 1 }); };
  var whiteStd = new THREE.MeshStandardMaterial({ color: 0xffffff, flatShading: true, roughness: 1 });
  placeMesh(cone, whiteStd, trees, function (c, it) { c.copy(it.c); });
  placeMesh(trunk, flat(0x5a3d2a), trunks);
  placeMesh(boxG, whiteStd, huts, function (c, it) { c.copy(it.c); });
  placeMesh(roofG, whiteStd, roofs, function (c, it) { c.copy(it.c); });
  var bldMat = litMaterial(0xffffff);
  placeMesh(boxG, bldMat, blds, function (c, it) { c.copy(it.c); });
  placeMesh(mountG, whiteStd, mounts, function (c, it) { c.copy(it.c); });
  placeMesh(cactusG, flat(0x4f7a3a), cacti);
  placeMesh(boxG, flat(0x3a332c), poles);

  /* landmarks: pyramids (Cairo), brick hall (Boston), India-gate style arch (Delhi), skyline lights */
  function landmark(i, build) { var g = new THREE.Group(); g.position.z = zStation(i); build(g); scene.add(g); return g; }
  /* window glow on city blocks follows the night factor */
  var glowMats = [];

  
  /* ---------- flags, banners, logo signs ---------- */
  function flagTex(code) {
    var c = document.createElement('canvas'); c.width = 300; c.height = 200; var g = c.getContext('2d');
    if (code === 'EG') { g.fillStyle = '#ce1126'; g.fillRect(0, 0, 300, 67); g.fillStyle = '#ffffff'; g.fillRect(0, 67, 300, 66); g.fillStyle = '#111'; g.fillRect(0, 133, 300, 67); g.fillStyle = '#c09300'; g.fillRect(135, 82, 30, 36); g.fillRect(128, 112, 44, 8); }
    else if (code === 'US') { for (var i = 0; i < 13; i++) { g.fillStyle = i % 2 ? '#ffffff' : '#b22234'; g.fillRect(0, i * 200 / 13, 300, 200 / 13 + 1); } g.fillStyle = '#3c3b6e'; g.fillRect(0, 0, 130, 108); g.fillStyle = '#fff'; for (var r = 0; r < 5; r++) for (var q = 0; q < 6; q++) { g.beginPath(); g.arc(12 + q * 20 + (r % 2) * 10, 12 + r * 19, 3, 0, 6.283); g.fill(); } }
    else { g.fillStyle = '#ff9933'; g.fillRect(0, 0, 300, 67); g.fillStyle = '#ffffff'; g.fillRect(0, 67, 300, 66); g.fillStyle = '#138808'; g.fillRect(0, 133, 300, 67); g.strokeStyle = '#000080'; g.lineWidth = 3; g.beginPath(); g.arc(150, 100, 28, 0, 6.283); g.stroke(); for (var k = 0; k < 24; k++) { var an = k * Math.PI / 12; g.beginPath(); g.moveTo(150, 100); g.lineTo(150 + Math.cos(an) * 28, 100 + Math.sin(an) * 28); g.stroke(); } }
    var t = new THREE.CanvasTexture(c); return t;
  }
  function bannerMesh(text, w, h, bg, fg) {
    var c = document.createElement('canvas'); c.width = 1024; c.height = Math.round(1024 * h / w); var g = c.getContext('2d');
    g.fillStyle = bg; g.fillRect(0, 0, c.width, c.height); g.strokeStyle = fg; g.lineWidth = 12; g.strokeRect(14, 14, c.width - 28, c.height - 28); g.fillStyle = fg; g.textAlign = 'center';
    var sz = 120; g.font = '800 ' + sz + 'px "Inter Tight", Arial, sans-serif'; while (g.measureText(text).width > c.width - 90 && sz > 30) { sz -= 6; g.font = '800 ' + sz + 'px "Inter Tight", Arial, sans-serif'; }
    g.fillText(text, c.width / 2, c.height / 2 + sz * .34);
    return new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshBasicMaterial({ map: new THREE.CanvasTexture(c), side: THREE.DoubleSide }));
  }
  var logoCache = {}, strips = [];
  function logoImg(k, cb) { var e = logoCache[k]; if (!e) { e = logoCache[k] = { img: new Image(), ok: false, cbs: [] }; e.img.onload = function () { e.ok = true; e.cbs.forEach(function (f) { f(); }); }; e.img.src = 'assets/logos/' + D.logos[k]; } if (!e.ok) e.cbs.push(cb); return e; }
  function makeStrip(keys) {
    var c = document.createElement('canvas'); c.width = 1024; c.height = 216; var g = c.getContext('2d'), tex = new THREE.CanvasTexture(c);
    function draw() {
      g.clearRect(0, 0, 1024, 216); var n = keys.length, tw = Math.min(190, (1024 - 24 * (n + 1)) / n), x0 = (1024 - (n * tw + (n - 1) * 24)) / 2;
      keys.forEach(function (k, i) {
        var x = x0 + i * (tw + 24); g.fillStyle = '#ffffff'; g.beginPath(); g.moveTo(x + 22, 14); g.arcTo(x + tw, 14, x + tw, 202, 22); g.arcTo(x + tw, 202, x, 202, 22); g.arcTo(x, 202, x, 14, 22); g.arcTo(x, 14, x + tw, 14, 22); g.fill();
        if (k === 'ted') { g.fillStyle = '#e62b1e'; g.font = '800 64px Arial'; g.textAlign = 'center'; g.fillText('TED', x + tw / 2 - 12, 125); g.fillStyle = '#111'; g.font = '800 40px Arial'; g.fillText('x', x + tw / 2 + 62, 125); return; }
        var e = logoCache[k]; if (e && e.ok) { var iw = e.img.naturalWidth || 200, ih = e.img.naturalHeight || 200, sc = Math.min((tw - 24) / iw, 150 / ih), dw = iw * sc, dh = ih * sc; try { g.drawImage(e.img, x + (tw - dw) / 2, 108 - dh / 2, dw, dh); } catch (er) {} }
      });
      tex.needsUpdate = true;
    }
    keys.forEach(function (k) { if (k !== 'ted') logoImg(k, draw); }); draw();
    return { tex: tex };
  }

  /* ---------- monuments: one per station ---------- */
  function monument(i, ch) {
    var side = i % 2 ? 1 : -1, g = new THREE.Group(), zc = zStation(i) - 26, ox = -side * 64;
    g.position.set(ox, hAt(ox, zc) + .2, zc);
    function box(w, h, d, x, y, z, hex) { var m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), typeof hex === 'number' ? flat(hex) : hex); m.position.set(x, y + h / 2, z); m.castShadow = true; m.receiveShadow = true; g.add(m); return m; }
    function cyl(rt, rb, h, x, y, z, hex, seg) { var m = new THREE.Mesh(new THREE.CylinderGeometry(rt, rb, h, seg || 12), flat(hex)); m.position.set(x, y + h / 2, z); m.castShadow = true; g.add(m); return m; }
    function cone(r, h, x, y, z, hex, seg, ry) { var m = new THREE.Mesh(new THREE.ConeGeometry(r, h, seg || 8), flat(hex)); m.position.set(x, y + h / 2, z); m.rotation.y = ry || 0; m.castShadow = true; g.add(m); return m; }
    function dome(r, x, y, z, hex) { var m = new THREE.Mesh(new THREE.SphereGeometry(r, 14, 8, 0, 6.283, 0, 1.5708), flat(hex)); m.position.set(x, y, z); m.castShadow = true; g.add(m); return m; }
    var k = ch.mon;
    box(46, 3, 46, 0, -3, 0, 0x6d655c);
    if (k === 'charminar') {
      var sand = 0xe8c9a0, dk = 0x4a3426;
      box(26, 13, 26, 0, 0, 0, sand); [[0, 13.3], [0, -13.3]].forEach(function (a) { box(9, 9, .8, a[0], 1, a[1], dk); box(.8, 9, 9, a[1], 1, a[0], dk); });
      box(18, 5, 18, 0, 13, 0, sand); [-1, 1].forEach(function (a) { [-1, 1].forEach(function (b2) { cyl(1.5, 2, 26, a * 12, 0, b2 * 12, sand, 10); cyl(2, 2, 1.2, a * 12, 18, b2 * 12, sand, 10); dome(2.2, a * 12, 19.2, b2 * 12, 0xd8b88a); cyl(.2, .2, 3, a * 12, 21.4, b2 * 12, 0xc9a24a, 6); dome(1.8, a * 7, 18, b2 * 7, 0xd8b88a); }); }); dome(5, 0, 18, 0, 0xd8b88a);
    } else if (k === 'pyramids') {
      [[0, 0, 28, 38], [-44, -26, 20, 26], [38, -34, 15, 19]].forEach(function (a) { cone(a[2], a[3], a[0], 0, a[1], 0xd9b56a, 4, Math.PI / 4); });
      box(14, 5, 6, -8, 0, 40, 0xd2a95f); box(5, 6, 5, -2, 5, 40, 0xd2a95f); box(3, 2, 7, -2, 0, 45.5, 0xc79c52); box(3, 2, 7, 2, 0, 45.5, 0xc79c52); box(6, 1.2, 5, -2, 11, 40, 0x2a4f8a);
      for (var pi = 0; pi < 6; pi++) { var px = 30 + pi * 4, pz = 30 + (pi % 2) * 5; cyl(.3, .45, 7, px, 0, pz, 0x6b4a2e, 6); for (var lf = 0; lf < 5; lf++) { var lm = new THREE.Mesh(new THREE.BoxGeometry(.5, .12, 4), flat(0x3f7a35)); lm.position.set(px, 7.2, pz); lm.rotation.set(-.4, lf * 1.256, 0); lm.translateZ(2); g.add(lm); } }
    } else if (k === 'temple') {
      var st = 0xe2c19a; [[22, 3], [17, 3], [12, 3], [8, 3]].forEach(function (a, n) { box(a[0], a[1], a[0], 0, n * 3, 0, st); }); cone(5, 10, 0, 12, 0, 0xd4a06a, 4, Math.PI / 4); cyl(.3, .3, 3, 0, 22, 0, 0xc9a24a, 6); box(34, 1.6, 34, 0, 0, 0, 0xf2e6d2).scale.y = .1;
    } else if (k === 'arch') {
      [-13, 13].forEach(function (x) { box(3.2, 22, 3.2, x, 0, 0, 0x8a3a2a); }); box(32, 4, 3.6, 0, 22, 0, 0x8a3a2a); var bn = bannerMesh('JAGRITI YATRA', 24, 5, '#0b1d3a', '#ffc83d'); bn.position.set(0, 16, 0); g.add(bn);
      for (var fl = -2; fl <= 2; fl++) box(.2, 6, .2, fl * 5, 26, 0, 0x222a38);
    } else if (k === 'mosque') {
      var cr = 0xe9d9bd; box(30, 12, 18, 0, 0, 0, cr); [-9, 0, 9].forEach(function (x) { box(6, 8, .7, x, 1, 9.2, 0x4a3a2c); }); dome(8, 0, 12, 0, 0xd9c9a8); dome(4, -10, 12, 0, 0xd9c9a8); dome(4, 10, 12, 0, 0xd9c9a8);
      [-17, 17].forEach(function (x) { cyl(1.2, 1.7, 28, x, 0, 8, cr, 8); cyl(2, 2, 1, x, 20, 8, cr, 8); dome(1.9, x, 21, 8, 0xd9c9a8); });
    } else if (k === 'morung') {
      [[-16, 0], [0, -6], [17, 2]].forEach(function (a, n) { box(9, 5, 13, a[0], 0, a[1], 0x6b4a2e); var rf = cone(10, 13 + n * 2, a[0], 5, a[1], 0xb89a54, 4, Math.PI / 4); rf.scale.z = 1.35; });
      [-5, 6].forEach(function (x) { cyl(.7, .9, 20, x, 0, 12, 0x4a2f1c, 7); box(2.4, 1.2, 3.4, x, 20, 12, 0xb5301f); });
    } else if (k === 'fort') {
      var fs = 0xd9a35c; box(46, 12, 3, 0, 0, -22, fs); box(46, 12, 3, 0, 0, 22, fs); box(3, 12, 46, -22, 0, 0, fs); box(3, 12, 46, 22, 0, 0, fs);
      [-22, 22].forEach(function (x) { [-22, 22].forEach(function (z2) { cyl(4.2, 4.8, 17, x, 0, z2, fs, 12); dome(4.4, x, 17, z2, 0xc89048); }); });
      var cren = new THREE.InstancedMesh(new THREE.BoxGeometry(1.4, 1.6, 1.4), flat(fs), 128), dm2 = new THREE.Object3D(), ci = 0; for (var t2 = -20; t2 <= 20; t2 += 2) { [[t2, -22], [t2, 22], [-22, t2], [22, t2]].forEach(function (a) { dm2.position.set(a[0], 12.8, a[1]); dm2.updateMatrix(); if (ci < 128) cren.setMatrixAt(ci++, dm2.matrix); }); } cren.count = ci; g.add(cren);
      box(18, 11, 18, 0, 0, 0, 0xe2b370); dome(6, 0, 11, 0, 0xc89048); box(8, 9, 1, 0, 0, 22.6, 0x4a3426);
    } else if (k === 'indiagate') {
      var pl = new THREE.Mesh(new THREE.PlaneGeometry(60, 60), flat(0x5f9a4f)); pl.rotation.x = -Math.PI / 2; pl.position.y = .05; g.add(pl);
      var gs = 0xc9a47a; [-9, 9].forEach(function (x) { box(8, 24, 10, x, 0, 0, gs); }); box(26, 7, 10, 0, 24, 0, gs); box(10, 20, 7, 0, 0, 0, 0x2a2420); box(30, 2, 11, 0, 31, 0, 0xb8946a); dome(3.4, 0, 33, 0, 0x8a6a4a); box(3, 1, 3, 0, 31, 0, 0xb8946a);
      [-24, 24].forEach(function (x) { box(10, .4, 40, x, 0, 4, 0x3a8fb0); });
    } else if (k === 'akshardham') {
      var ak = 0xf0c9a0; box(36, 5, 28, 0, 0, 0, 0xe8b88a); box(22, 14, 18, 0, 5, 0, ak); cone(9, 22, 0, 19, 0, 0xe2b080, 8); cone(2, 8, 0, 41, 0, 0xc9a24a, 8);
      [[-13, -10], [13, -10], [-13, 10], [13, 10]].forEach(function (a) { cyl(2, 2.6, 8, a[0], 5, a[1], ak, 10); cone(3.2, 7, a[0], 13, a[1], 0xe2b080, 8); });
    } else if (k === 'harvard') {
      var br = litMaterial(0xa4452f); box(36, 18, 22, 0, 0, 0, br); box(9, 34, 9, 0, 18, 12, br); cone(7.5, 12, 0, 52, 12, 0x2d3a4a, 4, Math.PI / 4); box(6, 1.2, .3, 0, 40, 16.6, 0xf2f0e8);
      box(12, 70, 12, 38, 0, -10, litMaterial(0x35547a)); cyl(.4, .4, 16, 38, 70, -10, 0xdddddd, 6);
    } else if (k === 'skyline') {
      var gl = [0x35547a, 0x41607f, 0x2a4a6a, 0x4a6f8a]; for (var tw = 0; tw < 14; tw++) box(8 + (tw % 3) * 3, 28 + ((tw * 37) % 55), 8 + (tw % 4) * 2, -34 + (tw % 5) * 17, 0, -22 + Math.floor(tw / 5) * 24, litMaterial(gl[tw % 4]));
    } else if (k === 'sunrise') {
      [-13, 13].forEach(function (x) { box(3.2, 22, 3.2, x, 0, 0, 0xc9a24a); }); box(32, 4, 3.6, 0, 22, 0, 0xc9a24a); var b3 = bannerMesh('NEXT STOP: YOU', 24, 5, '#ffc83d', '#0b1d3a'); b3.position.set(0, 16, 0); g.add(b3);
    }
    scene.add(g);
  }

  /* ---------- people and benches ---------- */
  var skin = [0xc68a5e, 0xa66c44, 0xe0ac7e, 0x8a5a3a], cloth = [0xe5483a, 0x19b3a6, 0xffc83d, 0x3a6fd0, 0xf6efe0, 0xff9a3c];
  function addPeople(g, side) {
    for (var j = 0; j < 6; j++) { var pz = (R() - .5) * 38, px = side * 10.6 + (R() - .5) * 2.6, body = new THREE.Mesh(new THREE.CylinderGeometry(.24, .3, 1.15, 7), flat(cloth[j % 6])); body.position.set(px, 1.4, pz); g.add(body); var head = new THREE.Mesh(new THREE.SphereGeometry(.22, 8, 6), flat(skin[j % 4])); head.position.set(px, 2.2, pz); g.add(head); }
    [-9, 9].forEach(function (z2) { var seat = new THREE.Mesh(new THREE.BoxGeometry(.7, .12, 2.2), flat(0x6b4a2e)); seat.position.set(side * 12, 1.2, z2); g.add(seat); var back = new THREE.Mesh(new THREE.BoxGeometry(.1, .7, 2.2), flat(0x6b4a2e)); back.position.set(side * 12.3, 1.6, z2); g.add(back); });
  }

  /* ---------- stations ---------- */
  var fontOK = true;
  function boardTex(txt, sub, hex) {
    var c = document.createElement('canvas'); c.width = 1024; c.height = 448; var g = c.getContext('2d');
    g.fillStyle = '#0b1d3a'; g.fillRect(0, 0, 1024, 448); g.fillStyle = hex; g.fillRect(0, 0, 1024, 26); g.fillRect(0, 422, 1024, 26);
    g.strokeStyle = '#f6efe0'; g.lineWidth = 10; g.strokeRect(20, 40, 984, 368);
    g.fillStyle = '#f6efe0'; g.textAlign = 'center';
    var sz = 150; g.font = '800 ' + sz + 'px "Inter Tight", Arial, sans-serif';
    while (g.measureText(txt).width > 880 && sz > 40) { sz -= 6; g.font = '800 ' + sz + 'px "Inter Tight", Arial, sans-serif'; }
    g.fillText(txt, 512, 238);
    g.fillStyle = hex; g.font = '500 44px "JetBrains Mono", monospace'; g.fillText(sub, 512, 330);
    var t = new THREE.CanvasTexture(c); t.anisotropy = 4; return t;
  }
  var lampPos = [], lampMat = new THREE.MeshBasicMaterial({ color: 0xffe3a0 }), boardRefs = [], palette = ['#ff9a3c', '#19b3a6', '#ffc83d', '#e5483a'], flags = [], lamps = [];
  var platMat = flat(0xc9c2b4), roofMat = flat(0x33415c), postMat = flat(0x222a38);
  D.chapters.forEach(function (ch, i) {
    var side = i % 2 ? 1 : -1, zc = zStation(i), g = new THREE.Group(); g.position.z = zc;
    var plat = new THREE.Mesh(new THREE.BoxGeometry(6, .8, 54), platMat); plat.position.set(side * 10.6, .4, 0); g.add(plat); addPeople(g, side);
    var roof = new THREE.Mesh(new THREE.BoxGeometry(6.4, .3, 32), roofMat); roof.position.set(side * 10.6, 5.2, 0); g.add(roof);
    [-14, 0, 14].forEach(function (pz) { var p = new THREE.Mesh(new THREE.BoxGeometry(.3, 4.6, .3), postMat); p.position.set(side * 8.2, 2.9, pz); g.add(p); lampPos.push(new THREE.Vector3(side * 8.2, 5, zc + pz + 2.2)); });
    var board = new THREE.Mesh(new THREE.PlaneGeometry(10, 4.4), new THREE.MeshBasicMaterial({ map: boardTex(ch.board, ch.sub || ch.year, palette[i % 4]), side: THREE.DoubleSide }));
    board.position.set(side * 14.5, 9.4, -8); board.rotation.y = -side * .8; g.add(board);
    [-1, 1].forEach(function (o) { var bp = new THREE.Mesh(new THREE.BoxGeometry(.35, 9, .35), postMat); bp.position.set(side * 14.5 + o * 3.4 * Math.cos(.8), 4.5, -8 + o * 3.4 * Math.sin(.8) * -side); g.add(bp); });
    var flag = new THREE.Mesh(new THREE.PlaneGeometry(3.6, 2.4, 10, 1), new THREE.MeshBasicMaterial({ map: flagTex(ch.country), side: THREE.DoubleSide })); flag.position.set(side * 11.3 + side * 1.8, 11.4, 12); flag.userData.side = side; g.add(flag); flags.push(flag);
    var pole = new THREE.Mesh(new THREE.CylinderGeometry(.09, .09, 11, 6), postMat); pole.position.set(side * 11.3, 6.3, 12); g.add(pole);
    if (ch.logos && ch.logos.length) { var strip = makeStrip(ch.logos), sm = new THREE.Mesh(new THREE.PlaneGeometry(10, 2.1), new THREE.MeshBasicMaterial({ map: strip.tex, transparent: true, side: THREE.DoubleSide })); sm.position.set(board.position.x, board.position.y - 3.35, board.position.z); sm.rotation.y = board.rotation.y; g.add(sm); }
    g.traverse(function (m) { if (m.isMesh) { m.castShadow = true; m.receiveShadow = true; } });
    monument(i, ch);
    scene.add(g); boardRefs.push({ mat: board.material, ch: ch, i: i });
  });
  var lampIM = new THREE.InstancedMesh(new THREE.SphereGeometry(.34, 8, 6), lampMat, lampPos.length), lo = new THREE.Object3D(); lampPos.forEach(function (lp, li) { lo.position.copy(lp); lo.updateMatrix(); lampIM.setMatrixAt(li, lo.matrix); }); lampIM.frustumCulled = false; scene.add(lampIM);
  if (document.fonts && document.fonts.load) document.fonts.load('800 80px "Inter Tight"').then(function () { return document.fonts.load('500 40px "JetBrains Mono"'); }).then(function () { boardRefs.forEach(function (r) { r.mat.map = boardTex(r.ch.board, r.ch.sub || r.ch.year, palette[r.i % 4]); r.mat.needsUpdate = true; }); }).catch(function () {});

  /* ---------- the train ---------- */
  var train = new THREE.Group(), wheels = [], smokeAnchor = new THREE.Object3D();
  var winMat = new THREE.MeshBasicMaterial({ color: 0xffe0a0 }); glowMats.push(winMat);
  function coach(zc, len, hex, engine) {
    var g = new THREE.Group(); g.position.z = zc;
    var body = new THREE.Mesh(new THREE.BoxGeometry(3.1, engine ? 3.2 : 3.4, len), flat(hex)); body.position.y = 2.7; g.add(body);
    var base = new THREE.Mesh(new THREE.BoxGeometry(2.8, .7, len - .6), flat(0x1c212b)); base.position.y = .75; g.add(base);
    var roofm = new THREE.Mesh(new THREE.BoxGeometry(2.6, .35, len - .4), flat(engine ? 0x1c212b : 0x2a3350)); roofm.position.y = engine ? 4.45 : 4.6; g.add(roofm);
    if (!engine) {
      var stripe = new THREE.Mesh(new THREE.BoxGeometry(3.14, .35, len + .02), flat(0xf6efe0)); stripe.position.y = 2.1; g.add(stripe);
      [-1, 1].forEach(function (zz2) { [-1, 1].forEach(function (sd3) { var dr = new THREE.Mesh(new THREE.BoxGeometry(.1, 2.4, 1.1), flat(0x1d2c4a)); dr.position.set(sd3 * 1.57, 2.5, zz2 * (len / 2 - 1.3)); g.add(dr); }); var vt = new THREE.Mesh(new THREE.CylinderGeometry(.3, .3, .3, 8), flat(0x2a3350)); vt.position.set(0, 4.9, zz2 * 2.2); g.add(vt); });
      for (var w = -3; w <= 3; w++) [-1, 1].forEach(function (sd) { var win = new THREE.Mesh(new THREE.PlaneGeometry(.85, .9), winMat); win.position.set(sd * 1.56, 3.4, w * (len / 8)); win.rotation.y = sd * Math.PI / 2; g.add(win); });
    }
    [-1, 1].forEach(function (zz) { [-1, 1].forEach(function (sd) { var wh = new THREE.Mesh(new THREE.CylinderGeometry(.62, .62, .28, 12), flat(0x20242c)); wh.rotation.z = Math.PI / 2; wh.position.set(sd * 1.35, .62, zz * (len / 2 - 1.5)); g.add(wh); wheels.push(wh); }); });
    return g;
  }
  var eng = coach(4, 8, 0xff8a2a, true);
  var chim = new THREE.Mesh(new THREE.CylinderGeometry(.35, .55, 1.6, 8), flat(0x1c212b)); chim.position.set(0, 5.1, -1.8); eng.add(chim);
  var boiler = new THREE.Mesh(new THREE.CylinderGeometry(1.35, 1.35, 4, 12), flat(0xf2f0e8)); boiler.rotation.x = Math.PI / 2; boiler.position.set(0, 3.1, -2.4); eng.add(boiler);
  var lampG = new THREE.Mesh(new THREE.SphereGeometry(.45, 10, 8), new THREE.MeshBasicMaterial({ color: 0xfff1b8 })); lampG.position.set(0, 3.3, -4.4); eng.add(lampG);
  smokeAnchor.position.set(0, 6.2, -1.8); eng.add(smokeAnchor);
  var cow = new THREE.Mesh(new THREE.BoxGeometry(2.6, .7, 1.8), flat(0x1c212b)); cow.position.set(0, .95, -4.7); cow.rotation.x = .45; eng.add(cow);
  var buf = new THREE.Mesh(new THREE.BoxGeometry(3.3, .5, .4), flat(0xb02a2a)); buf.position.set(0, 1.35, -4.3); eng.add(buf);
  var dome1 = new THREE.Mesh(new THREE.CylinderGeometry(.5, .62, .9, 10), flat(0xc9a24a)); dome1.position.set(0, 4.7, -.6); eng.add(dome1);
  var door = new THREE.Mesh(new THREE.CylinderGeometry(1.15, 1.15, .15, 14), flat(0x20242c)); door.rotation.x = Math.PI / 2; door.position.set(0, 3.1, -4.45); eng.add(door);
  var rods = [];
  [-1, 1].forEach(function (sd) { var rod = new THREE.Mesh(new THREE.BoxGeometry(.1, .16, 5), flat(0xb8bcc4)); rod.position.set(sd * 1.62, .62, 0); eng.add(rod); rods.push(rod); });
  var hl = new THREE.SpotLight(0xfff1b8, 0, 140, .5, .6); hl.position.set(0, 3.3, -4.5); hl.target.position.set(0, 1.5, -60); eng.add(hl); eng.add(hl.target);
  var beam = new THREE.Mesh(new THREE.ConeGeometry(6, 40, 14, 1, true), new THREE.MeshBasicMaterial({ color: 0xfff1b8, transparent: true, opacity: 0, blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.DoubleSide })); beam.rotation.x = Math.PI / 2; beam.position.set(0, 3, -24.6); eng.add(beam);
  train.add(eng);
  [0x2f67b8, 0x2a5aa2, 0x2f67b8].forEach(function (c, k) { train.add(coach(13.4 + k * 9.8, 9, c, false)); });
  train.userData.dyn = true; train.updateMatrixWorld(true);
  var tStatic = [], tWin = []; train.traverse(function (o) { if (!o.isMesh) return; if (o.material === winMat) tWin.push(o); else if (o.material.isMeshStandardMaterial && wheels.indexOf(o) < 0 && rods.indexOf(o) < 0) tStatic.push(o); });
  var tm1 = mergeMeshes(train, tStatic, sharedFlat, true); if (tm1) tm1.castShadow = true; mergeMeshes(train, tWin, winMat, false);
  wheels.forEach(function (w4) { w4.castShadow = !LOW; });
  scene.add(train);
  var smoke = [], smokeMat = new THREE.MeshBasicMaterial({ color: 0xeceef2, transparent: true, opacity: .6, depthWrite: false });
  for (var sm2 = 0; sm2 < (LOW ? 10 : 18); sm2++) { var pf = new THREE.Mesh(new THREE.SphereGeometry(.6, 7, 6), smokeMat.clone()); pf.visible = false; pf.userData.life = 1; scene.add(pf); smoke.push(pf); }

  /* ---------- clouds ---------- */
  var cloudG = new THREE.Group(), cloudMat = new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: .85, fog: false, depthWrite: false });
  for (var cI = 0; cI < (LOW ? 8 : 16); cI++) { var cg = new THREE.Group(); for (var q = 0; q < 4; q++) { var cm = new THREE.Mesh(new THREE.SphereGeometry(10 + R() * 8, 8, 6), cloudMat); cm.position.set(q * 12 - 18, R() * 4, R() * 6); cm.scale.y = .55; cg.add(cm); } cg.position.set((R() - .5) * 800, 90 + R() * 70, -R() * 700 + 100); cg.userData.sp = .5 + R() * 1.5; cloudG.add(cg); }
  cloudG.children.forEach(function (cg2) { mergeMeshes(cg2, cg2.children.slice(), cloudMat, false); });
  scene.add(cloudG);

  /* ---------- scenery: rivers, bridges, fields, turbines, crossings, signals ---------- */
  var water = [], rotors = [], crossings = [];
  RIVERS.forEach(function (rz) {
    var wm = new THREE.Mesh(new THREE.PlaneGeometry(380, 34), new THREE.MeshStandardMaterial({ color: 0x2f7fa6, transparent: true, opacity: .88, roughness: .15, metalness: .1 }));
    wm.rotation.x = -Math.PI / 2; wm.position.set(0, .14, rz); wm.receiveShadow = true; scene.add(wm); water.push(wm);
    var steel = flat(0x6a7480);
    [-1, 1].forEach(function (sd4) { var gd = new THREE.Mesh(new THREE.BoxGeometry(.5, 2.4, 38), steel); gd.position.set(sd4 * 7.7, 1.4, rz); gd.castShadow = true; scene.add(gd); for (var kk2 = -3; kk2 <= 3; kk2++) { var bx = new THREE.Mesh(new THREE.BoxGeometry(.3, 2.4, .3), steel); bx.position.set(sd4 * 7.7, 1.4, rz + kk2 * 5.4); scene.add(bx); } });
    [-14, -5, 5, 14].forEach(function (pz) { var pr = new THREE.Mesh(new THREE.BoxGeometry(15.4, 3.6, 1.6), flat(0x8a8378)); pr.position.set(0, -1.6, rz + pz); scene.add(pr); });
  });
  var fieldItems = [], fcol = [0x9fc25a, 0xd7c261, 0x6f9a45, 0xc9a45a, 0x8aa84a, 0xe3d28a];
  for (var fz = zmax; fz > zmin; fz -= 14) {
    var fb = bio(fvAtZ(fz)); if (fb.hut < .25 || fb.tree > .8) continue; var nearRiver = false; RIVERS.forEach(function (rz) { if (Math.abs(fz - rz) < 44) nearRiver = true; }); if (nearRiver) continue;
    for (var fs = -1; fs <= 1; fs += 2) if (R() < .75 * DEN) { var fx = fs * (22 + R() * 40), fw = 8 + R() * 8; fieldItems.push({ x: fx, y: hAt(fx, fz) + .1, z: fz, sx: fw, sy: 1, sz: fw * (.8 + R() * .9), c: new THREE.Color(fcol[Math.floor(R() * fcol.length)]) }); }
  }
  placeMesh(new THREE.BoxGeometry(1, .18, 1), whiteStd, fieldItems, function (c, it) { c.copy(it.c); });
  var towerM = flat(0xeef0f2), bladeM = flat(0xf6f6f6);
  for (var tb = 0; tb < (LOW ? 8 : 16); tb++) {
    var tz = tb < 6 ? Z0 - SP * (2.1 + R() * 1.0) : Z0 - SP * (6.2 + R() * 2.4), tsd = R() < .5 ? -1 : 1, tx = tsd * (46 + R() * 60), ty = hAt(tx, tz), tg2 = new THREE.Group(); tg2.position.set(tx, ty, tz);
    var tw2 = new THREE.Mesh(new THREE.CylinderGeometry(.5, .9, 30, 8), towerM); tw2.position.y = 15; tw2.castShadow = true; tg2.add(tw2);
    var nac = new THREE.Mesh(new THREE.BoxGeometry(2.2, 2, 4), towerM); nac.position.set(0, 30.5, 0); tg2.add(nac);
    var rot = new THREE.Group(); rot.userData.dyn = true; rot.position.set(0, 30.5, 2.4); for (var bl = 0; bl < 3; bl++) { var bm = new THREE.Mesh(new THREE.BoxGeometry(.7, 15, .2), bladeM); bm.geometry.translate(0, 7.5, 0); bm.rotation.z = bl * 2.094; bm.castShadow = true; rot.add(bm); } tg2.add(rot); scene.add(tg2); rotors.push({ g: rot, sp: .6 + R() * .6 });
  }
  CROSS.forEach(function (cz) {
    var cg = new THREE.Group(); cg.position.z = cz;
    var road = new THREE.Mesh(new THREE.PlaneGeometry(90, 7), flat(0x3a3a40)); road.rotation.x = -Math.PI / 2; road.position.y = .17; road.receiveShadow = true; cg.add(road);
    for (var dsh = -40; dsh <= 40; dsh += 6) { if (Math.abs(dsh) < 9) continue; var dm3 = new THREE.Mesh(new THREE.PlaneGeometry(2.6, .22), new THREE.MeshBasicMaterial({ color: 0xf2efe2 })); dm3.rotation.x = -Math.PI / 2; dm3.position.set(dsh, .19, 0); cg.add(dm3); }
    var piv = [], lamps2 = [];
    [-1, 1].forEach(function (sd5) {
      var pv = new THREE.Group(); pv.userData.dyn = true; pv.position.set(sd5 * 9.2, 1.0, 3.6); cg.add(pv); piv.push(pv);
      for (var sg = 0; sg < 6; sg++) { var seg = new THREE.Mesh(new THREE.BoxGeometry(.22, .22, 1.2), flat(sg % 2 ? 0xf2efe2 : 0xd23b2a)); seg.position.z = -.6 - sg * 1.2; pv.add(seg); }
      var post = new THREE.Mesh(new THREE.BoxGeometry(.4, 1.6, .4), postMat); post.position.set(sd5 * 9.2, .8, 3.6); cg.add(post);
      var lm = new THREE.Mesh(new THREE.SphereGeometry(.3, 8, 6), new THREE.MeshBasicMaterial({ color: 0x401010 })); lm.position.set(sd5 * 9.2, 2, 3.6); cg.add(lm); lamps2.push(lm);
      var car = new THREE.Group(); car.position.set(sd5 * 17, 0, 1.4 * sd5); var cb = new THREE.Mesh(new THREE.BoxGeometry(4, 1.2, 2), flat(sd5 > 0 ? 0xf2c230 : 0xd23b2a)); cb.position.y = 1; car.add(cb); var cab = new THREE.Mesh(new THREE.BoxGeometry(2, .9, 1.8), flat(0x9fc4d8)); cab.position.set(-.3, 1.9, 0); car.add(cab); car.traverse(function (m) { if (m.isMesh) m.castShadow = true; }); cg.add(car);
    });
    scene.add(cg); crossings.push({ z: cz, piv: piv, lamps: lamps2, amt: 0 });
  });
  for (var sg2 = 0; sg2 < 14; sg2++) { var gz = Z0 - 40 - sg2 * 110, sgp = new THREE.Mesh(new THREE.CylinderGeometry(.12, .15, 6, 6), postMat); sgp.position.set(6.4, 3, gz); scene.add(sgp); var sgb = new THREE.Mesh(new THREE.BoxGeometry(.6, 1.4, .4), flat(0x20242c)); sgb.position.set(6.4, 6.3, gz); scene.add(sgb); var sgl = new THREE.Mesh(new THREE.SphereGeometry(.22, 8, 6), new THREE.MeshBasicMaterial({ color: 0x35e07a })); sgl.position.set(6.4, 6.7, gz + .25); scene.add(sgl); }
  consolidateWorld();

  /* ---------- cards, index, navigation: one gesture = one stop ---------- */
  var card = $('card'), hero = $('hero'), hudEl = $('hud'), live = $('live'), pcount = $('pcount'), cutEl = $('cut'), idxEl = $('index'), sheet = $('sheet'), sheetBody = $('sheetBody'), bPrev = $('bPrev'), bNext = $('bNext'), bIndex = $('bIndex');
  var cur = 0, pos = 0, from = 0, to = 0, tStart = 0, moving = false, riding = false, jumped = false, sheetOpen = false, lastFocus = null;
  var rmq = window.matchMedia ? window.matchMedia('(prefers-reduced-motion: reduce)') : null;
  function isReduced() { return !!(rmq && rmq.matches); }
  function ease(k) { return k < .5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2; }
  var DUR = 1.7;
  var dots = document.createElement('span'); dots.className = 'dots';
  D.chapters.forEach(function (ch, i) { var b = document.createElement('button'); b.type = 'button'; b.setAttribute('data-go', i); b.setAttribute('aria-label', 'Go to ' + (i ? ch.label : 'the start')); b.title = i ? ch.label : 'Start'; dots.appendChild(b); });
  pcount.parentNode.insertBefore(dots, pcount.nextSibling);
  function setDisabled(b, off) { b.disabled = off; b.setAttribute('aria-disabled', off ? 'true' : 'false'); }
  function showStop(i, announce) {
    var ch = D.chapters[i];
    hudEl.classList.toggle('intro', i === 0);
    hero.classList.toggle('show', i === 0);
    card.classList.remove('show');
    if (i === 0) { card.textContent = ''; }
    else {
      var t = document.getElementById('t-' + ch.id); card.innerHTML = t ? t.innerHTML : '';
      card.classList.toggle('right', i % 2 === 0); card.scrollTop = 0; void card.offsetWidth; card.classList.add('show');
    }
    pcount.textContent = i === 0 ? 'Start' : String(i).padStart(2, '0') + ' / ' + String(N - 1).padStart(2, '0') + ' ' + ch.label;
    setDisabled(bPrev, i === 0); setDisabled(bNext, i === N - 1);
    var db = dots.children; for (var k = 0; k < db.length; k++) { db[k].classList.toggle('on', k === i); if (k === i) db[k].setAttribute('aria-current', 'step'); else db[k].removeAttribute('aria-current'); }
    var items = idxEl.querySelectorAll('button'); for (var q = 0; q < items.length; q++) { items[q].classList.toggle('on', q === i); if (q === i) items[q].setAttribute('aria-current', 'step'); else items[q].removeAttribute('aria-current'); }
    try { history.replaceState(null, '', i === 0 ? location.pathname + location.search : '#' + ch.id); } catch (e) {}
    if (announce) live.textContent = i === 0 ? 'Start of the journey.' : 'Station ' + i + ' of ' + (N - 1) + ': ' + ch.label + '. ' + ch.title;
  }
  function hideStop() { hero.classList.remove('show'); card.classList.remove('show'); hudEl.classList.remove('intro'); }
  function arrive(i) { pos = to = i; cur = i; moving = false; riding = false; showStop(i, true); if (soundOn) whistle(); }
  function cutTo(i, focusTitle) {
    if (moving) return false; moving = true; hideStop(); cutEl.classList.add('on');
    setTimeout(function () {
      pos = to = cur = i; jumped = true; moving = false; riding = false; cutEl.classList.remove('on'); showStop(i, true);
      if (focusTitle) { var h = card.querySelector('h2'); if (h) h.focus({ preventScroll: true }); }
    }, isReduced() ? 0 : 220);
    return true;
  }
  function go(i) {
    i = clamp(i, 0, N - 1); if (moving || sheetOpen || i === cur) return false;
    if (isReduced()) return cutTo(i);
    moving = true; riding = true; from = pos; to = i; tStart = -1; hideStop(); return true;
  }
  function open(i, viaIndex) { i = clamp(i, 0, N - 1); if (sheetOpen) closeCase(true); if (i === cur) return; if (Math.abs(i - cur) === 1 && !viaIndex) go(i); else cutTo(i, true); }
  /* case study sheet */
  function openCase(id, trigger) {
    var t = document.getElementById('c-' + id); if (!t) return;
    sheetBody.innerHTML = t.innerHTML; var im = sheetBody.querySelectorAll('img'); for (var k = 0; k < im.length; k++) im[k].loading = 'eager';
    lastFocus = trigger || document.activeElement; sheet.hidden = false; sheetOpen = true; sheet.scrollTop = 0; $('sheetX').focus({ preventScroll: true });
  }
  function closeCase(silent) { if (!sheetOpen) return; sheet.hidden = true; sheetOpen = false; sheetBody.textContent = ''; if (!silent && lastFocus && lastFocus.focus) lastFocus.focus({ preventScroll: true }); }
  $('sheetX').addEventListener('click', function () { closeCase(); });
  function closeIndex() { idxEl.hidden = true; bIndex.setAttribute('aria-expanded', 'false'); }
  bIndex.addEventListener('click', function () { var show = idxEl.hidden; idxEl.hidden = !show; bIndex.setAttribute('aria-expanded', show ? 'true' : 'false'); if (show) { var b = idxEl.querySelector('button.on') || idxEl.querySelector('button'); if (b) b.focus({ preventScroll: true }); } });
  bPrev.addEventListener('click', function () { go(cur - 1); });
  bNext.addEventListener('click', function () { go(cur + 1); });
  document.addEventListener('click', function (e) {
    var t = e.target; if (!t.closest) return;
    var ih = t.closest('.ih'); if (ih) { var box = ih.closest('.items'), all = box.querySelectorAll('.item'); for (var q2 = 0; q2 < all.length; q2++) { var on = all[q2] === ih.parentNode; all[q2].classList.toggle('open', on); all[q2].querySelector('.ih').setAttribute('aria-expanded', on ? 'true' : 'false'); } return; }
    var c = t.closest('[data-case]'); if (c) { e.preventDefault(); openCase(c.getAttribute('data-case'), c); return; }
    var b = t.closest('[data-go]'); if (b && !plainEl.contains(b)) { e.preventDefault(); var viaIdx = !!b.closest('#index'); closeIndex(); open(parseInt(b.getAttribute('data-go'), 10), viaIdx); }
  });

  /* input: wheel. A burst of wheel events (including trackpad momentum) is one gesture. */
  var lastWheelT = 0, lastMag = 0, gestureUsed = false;
  window.addEventListener('wheel', function (e) {
    if (e.ctrlKey || plainOn()) return;
    if (sheetOpen || (e.target.closest && e.target.closest('#index'))) return;
    e.preventDefault();
    var now = performance.now(), dy = e.deltaMode === 1 ? e.deltaY * 16 : e.deltaY, dx = e.deltaX, mag = Math.abs(dy) >= Math.abs(dx) ? Math.abs(dy) : Math.abs(dx), dir = (Math.abs(dy) >= Math.abs(dx) ? dy : dx) > 0 ? 1 : -1;
    var gap = now - lastWheelT, quiet = gap > 160, surge = gap > 50 && mag > lastMag * 1.7 + 30;
    lastWheelT = now; lastMag = mag;
    if (quiet) gestureUsed = false;
    if (mag < 4 || moving) return;
    if (gestureUsed && !surge) return;
    gestureUsed = true; go(cur + dir);
  }, { passive: false });
  /* input: touch swipe, one stop per swipe */
  var tx0 = 0, ty0 = 0, tOk = false;
  window.addEventListener('touchstart', function (e) {
    var t = e.target; tOk = !(plainOn() || sheetOpen || e.touches.length > 1 || (t.closest && t.closest('#index, button, a, input')));
    if (tOk) { tx0 = e.touches[0].clientX; ty0 = e.touches[0].clientY; }
  }, { passive: true });
  window.addEventListener('touchend', function (e) {
    if (!tOk) return; tOk = false; var t = e.changedTouches[0], dx = t.clientX - tx0, dy = t.clientY - ty0;
    if (Math.max(Math.abs(dx), Math.abs(dy)) < 52) return;
    if (Math.abs(dy) >= Math.abs(dx)) go(cur + (dy < 0 ? 1 : -1)); else go(cur + (dx < 0 ? 1 : -1));
  }, { passive: true });
  /* input: keyboard */
  window.addEventListener('keydown', function (e) {
    if (e.altKey || e.ctrlKey || e.metaKey) return;
    if (e.key === 'Escape') { if (sheetOpen) { closeCase(); e.preventDefault(); } else if (!idxEl.hidden) { closeIndex(); bIndex.focus(); } return; }
    if (sheetOpen) {
      if (e.key === 'Tab') { var f = sheet.querySelectorAll('button,a[href]'), first = f[0], last = f[f.length - 1]; if (!f.length) return; if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); } else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); } }
      return;
    }
    if (plainOn()) return;
    var tag = (e.target.tagName || '').toLowerCase(), onCtl = tag === 'button' || tag === 'a' || tag === 'input' || tag === 'summary';
    var k = e.key, next = k === 'ArrowDown' || k === 'ArrowRight' || k === 'PageDown' || (k === ' ' && !e.shiftKey && !onCtl), prev = k === 'ArrowUp' || k === 'ArrowLeft' || k === 'PageUp' || (k === ' ' && e.shiftKey && !onCtl);
    if (onCtl && (k === 'ArrowDown' || k === 'ArrowUp') && e.target.closest && e.target.closest('#index')) { var bs = Array.prototype.slice.call(idxEl.querySelectorAll('button')), ix = bs.indexOf(e.target); var nx = bs[clamp(ix + (k === 'ArrowDown' ? 1 : -1), 0, bs.length - 1)]; if (nx) { e.preventDefault(); nx.focus(); } return; }
    if (onCtl && (k === 'ArrowLeft' || k === 'ArrowRight')) return;
    if (next) { e.preventDefault(); go(cur + 1); } else if (prev) { e.preventDefault(); go(cur - 1); }
    else if (k === 'Home') { e.preventDefault(); open(0, true); } else if (k === 'End') { e.preventDefault(); open(N - 1, true); }
  });
  window.addEventListener('hashchange', function () { var h = location.hash.replace('#', ''); for (var i = 0; i < N; i++) if (D.chapters[i].id === h && i !== cur) { open(i, true); return; } });

  /* ---------- sound (synthesised, off by default) ---------- */
  var ac = null, soundOn = false, master = null;
  function snd() {
    if (!ac) { var AC = window.AudioContext || window.webkitAudioContext; if (!AC) return false; ac = new AC(); master = ac.createGain(); master.gain.value = .5; master.connect(ac.destination); }
    if (ac.state === 'suspended') ac.resume(); return true;
  }
  function clack(vol) { if (!soundOn || !ac) return; var b = ac.createBuffer(1, 1500, ac.sampleRate), d = b.getChannelData(0); for (var i = 0; i < d.length; i++) d[i] = (Math.random() * 2 - 1) * (1 - i / d.length); var s = ac.createBufferSource(), f = ac.createBiquadFilter(), g = ac.createGain(); s.buffer = b; f.type = 'bandpass'; f.frequency.value = 900; g.gain.value = vol; s.connect(f); f.connect(g); g.connect(master); s.start(); }
  function tone(freq, dur, type, vol) { if (!soundOn || !ac) return; var o = ac.createOscillator(), g = ac.createGain(); o.type = type || 'triangle'; o.frequency.value = freq; g.gain.setValueAtTime(vol || .08, ac.currentTime); g.gain.exponentialRampToValueAtTime(.0001, ac.currentTime + dur); o.connect(g); g.connect(master); o.start(); o.stop(ac.currentTime + dur); }
  function whistle() { tone(392, .5, 'sawtooth', .05); setTimeout(function () { tone(523, .7, 'sawtooth', .05); }, 220); }
  $('bSound').addEventListener('click', function () { soundOn = !soundOn; if (soundOn && !snd()) soundOn = false; this.setAttribute('aria-pressed', soundOn ? 'true' : 'false'); $('sndTxt').textContent = soundOn ? 'sound: on' : 'sound: off'; if (soundOn) tone(660, .2); });
  function plainOn() { return root.classList.contains('plain-on'); }

  /* ---------- main loop ---------- */
  var frameCount = 0, prevZ = Z0, speed = 0, clock = new THREE.Clock(), W = 0, Hh = 0, soundDist = 0;
  function resize() { W = window.innerWidth; Hh = window.innerHeight; renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, prCap)); renderer.setSize(W, Hh, false); camera.aspect = W / Hh; camera.updateProjectionMatrix(); }
  window.addEventListener('resize', resize); resize();
  function start() { started = true; clock.start(); }
  var tgt = new THREE.Vector3(), sd = new THREE.Vector3();
  function frame() {
    if (!running) return;
    var rawDt = clock.getDelta(), dt = Math.min(rawDt, .05), time = clock.elapsedTime, amb = isReduced() ? 0 : 1;
    fsum += rawDt; if (++frameN >= 75) { var avg = fsum / frameN; frameN = 0; fsum = 0; if (avg > .034 && qLevel < 3) { qLevel++; if (qLevel === 1) { prCap = Math.max(.8, prCap - .4); resize(); } else if (qLevel === 2) { sun.castShadow = false; prCap = Math.max(.75, prCap - .25); resize(); } else { cloudG.visible = false; } } }
    if (LOW || qLevel > 0) { renderer.shadowMap.autoUpdate = false; renderer.shadowMap.needsUpdate = (frameCount++ % 3) === 0; }
    if (riding) { if (tStart < 0) tStart = time; var kk = clamp((time - tStart) / DUR, 0, 1); pos = from + (to - from) * ease(kk); if (kk >= 1) arrive(to); }
    var fv = pos, z = Z0 - fv * SP, dz = jumped ? 0 : z - prevZ; jumped = false; prevZ = z; speed += ((Math.abs(dz) / Math.max(dt, .001)) - speed) * .15;
    train.position.set(0, 0, z);
    for (var mb = 0; mb < mergedBuckets.length; mb++) mergedBuckets[mb].visible = Math.abs(mergedBuckets[mb].userData.zc - z) < 640;
    wheels.forEach(function (wh) { wh.rotation.x -= dz * 1.6; });
    /* camera: platform view at the start, follow view once the train has left */
    var port = W / Hh < .8, back = port ? 58 : 47, hgt = port ? 12 : 8.8, ipc = smooth(0, 1, pos);
    var cx0 = (port ? -66 : -64) + Math.sin(time * .35) * .6 * amb, cy0 = (port ? 9 : 6.5) + Math.sin(time * .27) * .12 * amb, cz0 = z + 12;
    camera.position.set(lerp(cx0, 0, ipc), lerp(cy0, hgt, ipc), lerp(cz0, z + back, ipc));
    tgt.set(lerp(0, 0, ipc), lerp(2.6, 3.2, ipc), lerp(z + 15, z - 22, ipc)); camera.lookAt(tgt);
    camera.fov = lerp(port ? 52 : 38, port ? 74 : 62, ipc);
    /* at the start the train sits in the free part of the screen: right and low on desktop, low on phones */
    var vk = 1 - ipc; if (vk > .002) camera.setViewOffset(W, Hh, port ? 0 : -W * .1 * vk, -Hh * (port ? .3 : .2) * vk, W, Hh); else camera.clearViewOffset();
    camera.updateProjectionMatrix();
    /* biome atmosphere */
    var b = bio(fv), sy = b.sunY;
    sd.set(.35, Math.max(sy, -.25), -.9).normalize();
    sky.position.copy(camera.position); sky.material.uniforms.top.value.copy(b.top); sky.material.uniforms.hor.value.copy(b.hor); sky.material.uniforms.sunDir.value.copy(sd); sky.material.uniforms.sunC.value.copy(b.sunC).multiplyScalar(.5);
    sunMesh.position.copy(camera.position).addScaledVector(sd, 760); sunMesh.material.color.copy(b.sunC); sunMesh.visible = sy > -.05;
    scene.fog.color.copy(b.hor); scene.fog.near = b.fogN; scene.fog.far = b.fogF;
    hemi.color.copy(b.top).lerp(tmpA.set(0xffffff), .45); hemi.groundColor.copy(b.g1).multiplyScalar(.6); hemi.intensity = b.hemi;
    sun.color.copy(b.sunC); sun.intensity = b.sunI; sun.position.set(camera.position.x + sd.x * 120, camera.position.y + Math.max(sd.y, .15) * 120, z + sd.z * 120); sun.target.position.set(0, 0, z);
    stars.position.copy(camera.position); stars.material.opacity = b.star * .95;
    var glow = b.glow; winMat.color.setRGB(1, .86 - (1 - glow) * .2, .6 + (1 - glow) * .3).multiplyScalar(.45 + glow * .6); lampMat.color.setRGB(1, .85 + Math.sin(time * 3) * .05 * amb, .55).multiplyScalar(.5 + glow * .5);
    cloudG.position.set(0, 0, camera.position.z * .96); cloudG.children.forEach(function (c) { c.position.x += c.userData.sp * dt * amb; if (c.position.x > 420) c.position.x = -420; });
    cloudMat.opacity = .55 + (b.sunI > .6 ? .35 : 0); cloudMat.color.copy(b.hor).lerp(tmpA.set(0xffffff), .6);
    if (amb) flags.forEach(function (fl, i) { var pa = fl.geometry.attributes.position, sdd = fl.userData.side; for (var v2 = 0; v2 < pa.count; v2++) { var x0 = pa.getX(v2), kk2 = sdd > 0 ? (x0 + 1.8) / 3.6 : (1.8 - x0) / 3.6; pa.setZ(v2, Math.sin(time * 4 + kk2 * 6 + i) * .4 * kk2); } pa.needsUpdate = true; });
    /* smoke */
    var anchor = new THREE.Vector3(); smokeAnchor.getWorldPosition(anchor);
    smoke.forEach(function (pf, i) {
      var L = pf.userData.life; if (L >= 1) { if (amb && Math.random() < dt * (1.2 + clamp(speed * .12, 0, 8))) { pf.userData.life = 0; pf.position.copy(anchor); pf.position.x += (Math.random() - .5) * .3; pf.visible = true; } return; }
      pf.userData.life = L + dt * .55; pf.position.y += dt * 3.2; pf.position.z += dt * (4 + speed * .1); pf.position.x += Math.sin(time + i) * dt * .6; var sc = 1 + L * 2.2; pf.scale.setScalar(sc); pf.material.opacity = (1 - L) * .55; if (pf.userData.life >= 1) pf.visible = false;
    });
    water.forEach(function (w3) { w3.material.color.setHex(0x2f7fa6).lerp(b.hor, .4); });
    rotors.forEach(function (r) { r.g.rotation.z += dt * r.sp * amb; });
    var wa = wheels.length ? -wheels[0].rotation.x : 0; rods.forEach(function (r) { r.position.y = .62 + Math.sin(wa) * .3; r.position.z = Math.cos(wa) * .3; });
    crossings.forEach(function (cx) { var ahead = z - cx.z, want = (ahead < 100 && ahead > -48) ? 1 : 0; cx.amt += (want - cx.amt) * Math.min(1, dt * 2.2); cx.piv.forEach(function (pv) { pv.rotation.x = (1 - cx.amt) * 1.25; }); cx.lamps.forEach(function (l, li) { l.material.color.setHex(cx.amt > .1 && (amb ? Math.sin(time * 9 + li * 3.1) > 0 : li === 0) ? 0xff3a2a : 0x401010); }); });
    hl.intensity = clamp(1 - b.sunI * .85, 0, 1) * 2.6; beam.material.opacity = clamp(1 - b.sunI * .95, 0, 1) * .09;
    litShaders.forEach(function (sh) { sh.uniforms.uGlow.value = glow; });
    soundDist += Math.abs(dz); if (soundDist > 3.6) { soundDist = 0; if (speed > 2) clack(clamp(speed * .004, .02, .14)); }
    renderer.render(scene, camera);
    window.requestAnimationFrame(frame);
  }
  if (/[?&]debug/.test(location.search)) window.__yatra = { get cur() { return cur; }, get pos() { return pos; }, get moving() { return moving; }, go: go, open: open, get q() { return { LOW: LOW, qLevel: qLevel, prCap: prCap, calls: renderer.info.render.calls, tris: renderer.info.render.triangles }; } };
  window.scrollTo(0, 0);
  /* start where the URL says (deep links), else at the platform */
  (function () { var h = location.hash.replace('#', ''); for (var i = 1; i < N; i++) if (D.chapters[i].id === h) { cur = pos = to = i; prevZ = Z0 - i * SP; } })();
  setPlain(false);
  showStop(cur, false);
})();
