const listElement = document.getElementById('list');
if (listElement) {
  listElement.innerHTML = `
    <div class="row row-cols-1 row-cols-md-3 g-4">
      <div class="col">
        <div class="card">
        <img src="..." class="card-img-top" alt="...">
        <div class="card-body">
          <h5 class="card-title">Card title</h5>
        </div>
      </div>
      <div class="col"></div>
      <div class="col"></div>
    </div>
  `;
}

//TODO: list라는 ID를 가진 얘 한테 <div class="row row-cols-1 row-cols-md-3 g-4"> 넣기, 반복문으로 n개의 col 넣기