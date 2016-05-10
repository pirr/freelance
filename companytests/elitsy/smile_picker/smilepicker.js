$(function(){

    var SmilePicker = Backbone.View.extend({

        el: '.smile-picker',

        events: {
            'click #send': 'sendMessage',
        },

        initialize: function() {
            this.initializeEmoji();
            window.emojioneVersion = "2.1.1";
        },

        initializeEmoji: function() {
            // this.getEmojiJson();
            emojione.imagePathPNG = 'assets/png/';
            emojione.ascii = true;
            // var emojioneList = 
            
            $('#txt').emojioneArea({
                pickerPosition: 'right',
            });
        },

        sendMessage: function() {
            
            var input = document.getElementById('txt').value;
            var output = emojione.shortnameToImage(input);
            document.getElementById('outputText').innerHTML = output;
        }
    });

    var smilePicker = new SmilePicker();
})