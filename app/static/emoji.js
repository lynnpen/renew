window.onload = function() {
    var hi = new hichat();
	hi.init();
};
var hichat = function () {

};


var emojiArray = new Array('', '微笑', '撇嘴', '色', '发呆', '流泪', '害羞', '闭嘴', '睡', '大哭', '尴尬', '发怒', '调皮', '呲牙', '惊讶', '难过', '冷汗', '抓狂', '吐', '偷笑', '愉快', '白眼', '傲慢', '饥饿', '困', '惊恐', '流汗', '憨笑', '悠闲', '奋斗', '咒骂', '疑问', '嘘', '晕', '疯了', '衰', '敲打', '再见', '擦汗', '抠鼻', '糗大了', '坏笑', '左哼哼', '右哼哼', '哈欠', '鄙视', '委屈', '快哭了', '阴险', '亲亲', '吓', '可怜', '拥抱', '月亮', '太阳', '炸弹', '骷髅', '菜刀', '猪头', '西瓜', '咖啡', '饭', '爱心', '强', '弱', '握手', '胜利', '抱拳', '勾引', 'OK', 'NO', '玫瑰', '凋谢', '嘴唇', '爱情', '飞吻')

hichat.prototype = {
	init: function() {
		this._initialEmoji();
		document.getElementById('emoji').addEventListener('click', function(e) {
			var emojiwrapper = document.getElementById('emojiWrapper');
			emojiwrapper.style.display = 'block';
			e.stopPropagation();
		}, false);
		document.body.addEventListener('click', function(e) {
			var emojiwrapper = document.getElementById('emojiWrapper');
			if (e.target != emojiwrapper) {
				emojiwrapper.style.display = 'none';
		   };  
		}); 
		document.getElementById('emojiWrapper').addEventListener('click', function(e) {
			//获取被点击的表情
			var target = e.target;
			if (target.nodeName.toLowerCase() == 'img') {
				var messageInput = document.getElementById('m');
				messageInput.focus();
				emojiName = emojiArray[target.title];
				messageInput.value = messageInput.value + '[' + emojiName + ']';
			};  
		}, false);

	},
	_initialEmoji: function () {
		var emojiContainer = document.getElementById('emojiWrapper'),
			docFragment = document.createDocumentFragment();
		for (var i = 75; i > 0; i--) {
			var emojiItem = document.createElement('img');
			emojiItem.src = 'static/face/' + i + '.gif';
			emojiItem.title = i;
			docFragment.appendChild(emojiItem);
		};
		emojiContainer.appendChild(docFragment);
	}
};
