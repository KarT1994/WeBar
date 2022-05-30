flg = 0;
scale_num = 10;
num_text = String(scale_num);
scale_text = "50 50 50";
tick_cnt = 0;
device_latitude = "none";
device_longitude = "none";
place_text = "latitude: 0.0; longitude: 0.0;"
dis = "0"


var ws = new WebSocket('wss://' + window.location.host + '/ws/');
ws.onmessage = function(e) {
  var data = JSON.parse(e.data);

  //配列を2重ループで初期化する場合
   let shops_array = new Array(5);

    for(let i=0; i<5; i++)
    {
      shops_array[i] = new Array(5);
      for(let j=0; j<5; j++)
      {
        shops_array[i][0] = data['message'+i];
        shops_array[i][1] = data['shop_lat'+i];
        shops_array[i][2] = data['shop_lng'+i];
        shops_array[i][3] = data['shop_dis'+i];
        shops_array[i][4] = data['catch'+i];
        shops_array[i][5] = data['urls'+i];
      }
    }

    console.log(shops_array[0]);
    console.log(shops_array[0][0]);
    console.log(shops_array[1][0]);
    console.log(shops_array[0][1]);

    for(let shop_cnt=0; shop_cnt<5; shop_cnt++)
    {
      var shop_name = shops_array[shop_cnt][0];
      var shop_catch  = shops_array[shop_cnt][4];
      var _size   = 400 / Number(shops_array[shop_cnt][3]);
      var shop_lat = shops_array[shop_cnt][1];
      var shop_lng = shops_array[shop_cnt][2];
      var shop_url = shops_array[shop_cnt][5];

      if(shop_catch == "")
      {
        text = shop_name;
      }
      else
      {
        text = shop_catch;
      }

      var text_cnt = text.length;
      var width = text_cnt*14;
      var height= 16;
      let cvs = document.createElement('canvas');
      let ctx = cvs.getContext('2d');
      cvs.width = width*10;
      cvs.height = height*10;
      ctx.fillStyle = "rgb(221, 255, 255)";
      ctx.fillRect(10,20,6000,3000);
      
      ctx.fillStyle = "rgb(51, 51, 51)";
      ctx.font = '100pt Arial';
      ctx.fillText(text,0,125);
      
      var base64 = cvs.toDataURL("image/png");

      document.querySelector('#test'+shop_cnt).innerHTML = `
      <a-entity gps-entity-place="latitude: ${(shop_lat)}; longitude: ${(shop_lng)};">
      <a-image 
      scale="${(width)/_size} ${height/_size} 1" src="${base64}"  
      look-at="[gps-camera]"
      >
      </a-image>
      <a-entity position="0 -10 0">
      <a-octahedron color="#FFF100" radius="5"></a-octahedron>
      </a-entity>
      </a-entity>
      `

      if(shop_url == "")
      {
        document.getElementById("menu_shop"+shop_cnt).innerHTML=
        `<a class="menu-shop-catch">${shop_catch}<br></a>
        <a tabindex="-1" target="_blank" rel="noopener noreferrer">${shop_name}</a>`;
      }
      else
      {
        document.getElementById("menu_shop"+shop_cnt).innerHTML=
        `<a class="menu-shop-catch">${shop_catch}<br></a>
        <a href="${shop_url}" target="_blank" rel="noopener noreferrer">${shop_name}</a>`;
      }
    }
};

ws.onclose = function(e) {
  msg = 'websocket closed';
}


/****************************/
// 位置情報取得
/****************************/
  var my_latitude = '0.0';
  var my_longitude = '0.0';
  function test() {
      navigator.geolocation.getCurrentPosition(test2);
  }

  function test2(position) {
      my_latitude = position.coords.latitude;
      my_longitude = position.coords.longitude;

  }
  // csrf_tokenの取得

  $(function() {

    setInterval(function(){
      test();
      const sendData = {
        message : my_latitude + "," + my_longitude
      }
      ws.send(JSON.stringify(sendData));
      },10000);
  });


