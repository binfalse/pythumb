$( document ).ready(function() {

	/* Sidebar height set */
	$('.sidebar').css('min-height',$(document).height());

	/* Secondary contact links */
	var scontacts = $('#contact-list-secondary');
	var contact_list = $('#contact-list');
	
	scontacts.hide();
	
	contact_list.mouseenter(function(){ scontacts.fadeIn(); });
	
	contact_list.mouseleave(function(){ scontacts.fadeOut(); });

    if ($('#ctlist').length)
    {
        $('#ctlist').css('height', $(document).height() - 250);
        if(window.location.hash)
        {
            var hash = window.location.hash;
            if ($(hash).length)
                $(hash).addClass ("active");
        }
    }

});
