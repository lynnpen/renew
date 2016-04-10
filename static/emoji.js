window.onload = function() {
    var hi = new hichat();
	hi.init();
};
var hichat = function () {
    
};
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
				messageInput.value = messageInput.value + '[emoji:' + target.title + ']';
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
