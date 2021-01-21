document.on('ready', function(){
    var hiddenMenuItems = document.getElementsByClassName('hidden');
    console.log(hiddenMenuItems);
    hiddenMenuItems.on('focus', function(){
        this.removeClass('hidden');
    });
})