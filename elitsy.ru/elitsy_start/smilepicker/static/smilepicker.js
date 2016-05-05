$(function(){

    var SmilePicker = Backbone.View.extend({

        el: '.smile-picker',

        events: {
            'click a': 'openSmilesPopup',
            'click .smile': 'insertSmile'
        },

        openSmilesPopup: function() {
            console.log("click")
            $('.smiles_popup').toggle();
        },

        insertSmile: function(e) {
            smile = $(e.currentTarget).text();
            var caretPos = document.getElementById("txt").selectionStart;
            var textAreaTxt = $('#txt').val();
            $('#txt').val(textAreaTxt.substring(0, caretPos) + 
                smile + textAreaTxt.substring(caretPos));
        },
    });

    var smilePicker = new SmilePicker();
})