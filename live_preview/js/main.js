/* Three.js animated particle / subtle metallic glow + model grid generation */
(() => {
  const canvas = document.getElementById('bg-canvas');
  function resize() { canvas.width = innerWidth; canvas.height = innerHeight; renderer.setSize(innerWidth, innerHeight); camera.aspect = innerWidth/innerHeight; camera.updateProjectionMatrix(); }
  const renderer = new THREE.WebGLRenderer({canvas: canvas, alpha: true});
  renderer.setSize(innerWidth, innerHeight); renderer.setPixelRatio(Math.min(window.devicePixelRatio||1,1.5));
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(60, innerWidth/innerHeight, 0.1, 1000);
  camera.position.z = 70;

  // particulate geometry
  const COUNT = 1400;
  const positions = new Float32Array(COUNT * 3);
  const colors = new Float32Array(COUNT * 3);
  for(let i=0;i<COUNT;i++){
    positions[3*i] = (Math.random()-0.5)*220;
    positions[3*i+1] = (Math.random()-0.5)*140;
    positions[3*i+2] = (Math.random()-0.5)*260;
    // bluish metallic color variation
    const t = Math.random()*0.5 + 0.5;
    colors[3*i] = 10/255 * t;   // r small
    colors[3*i+1] = 99/255 * t; // g bluish
    colors[3*i+2] = 255/255 * t;// b strong
  }
  const geom = new THREE.BufferGeometry();
  geom.setAttribute('position', new THREE.BufferAttribute(positions,3));
  geom.setAttribute('color', new THREE.BufferAttribute(colors,3));
  const mat = new THREE.PointsMaterial({size:1.8, vertexColors:true, transparent:true, opacity:0.14});
  const points = new THREE.Points(geom, mat);
  scene.add(points);

  // ambient gentle light sheen plane (faint metallic band)
  const planeGeo = new THREE.PlaneGeometry(800,400);
  const planeMat = new THREE.MeshBasicMaterial({color: 0x062f7f, transparent:true, opacity:0.02});
  const plane = new THREE.Mesh(planeGeo, planeMat);
  plane.position.z = -120; scene.add(plane);

  function tick(){
    points.rotation.y += 0.0009;
    points.rotation.x += 0.0005;
    renderer.render(scene,camera);
    requestAnimationFrame(tick);
  }
  tick();
  window.addEventListener('resize', resize);
})();

/* Cards data: 4 models — precise, auditable, ready */
const MODELS = [
  {id:'KAI-001', title:'Keystone Model Alpha', price:'$199.99', img:'images/model1.jpg'},
  {id:'KAI-002', title:'Keystone Model Beta',  price:'$199.99', img:'images/model2.jpg'},
  {id:'KAI-003', title:'Keystone Model Gamma', price:'$299.99', img:'images/model3.jpg'},
  {id:'KAI-004', title:'Keystone Model Delta', price:'$399.99', img:'images/model4.jpg'}
];

function buildCards(){
  const container = document.getElementById('models');
  container.innerHTML = '';
  MODELS.forEach(m=>{
    const card = document.createElement('article'); card.className='card';
    card.innerHTML = `
      <img src="${m.img}" alt="${m.title}">
      <h3>${m.title}</h3>
      <div class="price">${m.price}</div>
      <div class="controls">
        <button class="paypal" data-paypal-id="${m.id}">PayPal</button>
        <button class="stripe" data-stripe-id="${m.id}">Stripe</button>
      </div>
    `;
    container.appendChild(card);
  });
  gsap.from('.card', {y:20, opacity:0, stagger:0.06, duration:0.6, ease:'power3.out'});
}

document.addEventListener('DOMContentLoaded', ()=>{
  buildCards();

  document.body.addEventListener('click', e=>{
    if(e.target.matches('.paypal')){
      const id = e.target.dataset.paypalId;
      // hosted_button_id placeholder — replace with your real hosted IDs in production
      window.location.href = `https://www.paypal.com/checkoutnow?hosted_button_id=${encodeURIComponent(id)}`;
    }
    if(e.target.matches('.stripe')){
      const id = e.target.dataset.stripeId;
      alert('Stripe checkout placeholder for: ' + id + '\nWhen ready we will wire server-side checkout sessions.');
    }
  });
});
