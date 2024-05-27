onload = function() {
    draw_green();
    var canvas = document.getElementById('canvassample');
    if ( ! canvas || ! canvas.getContext ) {
	return false;
    }
    var ctx = canvas.getContext('2d');
    console.log("width= " + canvas.width + " height= " + canvas.height);
    ctx.fillStyle = "rgb(55, 55, 55)";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
}
function draw_red() {
    /* canvas要素のノードオブジェクト */
    var canvas = document.getElementById('canvassample');
    /* canvas要素の存在チェックとCanvas未対応ブラウザの対処 */
    if ( ! canvas || ! canvas.getContext ) {
	return false;
    }
    /* 2Dコンテキスト */
    var ctx = canvas.getContext('2d');
    /* 四角を描く */
    ctx.beginPath();
    ctx.fillStyle = 'rgb(192, 80, 77)'; // 赤
    ctx.arc(17, 20, 15, 0, Math.PI*2, false);
    ctx.fill();
}

function draw_green() {
    var canvas = document.getElementById('canvassample');
    if ( ! canvas || ! canvas.getContext ) {
	return false;
    }
    var ctx = canvas.getContext('2d');
    ctx.beginPath();
    ctx.fillStyle = 'rgb(155, 187, 89)'; // GREEN
    ctx.arc(17, 20, 15, 0, Math.PI*2, false);
    ctx.fill();
}


function draw_text(val) {
    console.log("draw_text= " + val);
    var canvas = document.getElementById('canvassample');
    if ( ! canvas || ! canvas.getContext ) {
	return false;
    }
    var ctx = canvas.getContext('2d');

    ctx.fillStyle = "rgb(255, 255, 255)";
    ctx.fillRect(34, 0, 140, 40);

    ctx.font= 'bold 24px Century Gothic';
    ctx.strokeStyle = '#00A3D9';
    ctx.lineWidth = 6; 
    ctx.lineJoin = 'round';
    ctx.fillStyle = '#fff';
    ctx.strokeText(val+" WHr",40,30,140);
    ctx.fillText(val+" WHr",40,30);
}

