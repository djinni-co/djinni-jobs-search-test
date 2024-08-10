$(document).ready(function() {
    window.toggleDescription = function(jobId) {
      var $shortDesc = $('#short_' + jobId);
      var $fullDesc = $('#full_' + jobId);

      if ($shortDesc.hasClass('d-none')) {
        $shortDesc.removeClass('d-none');
        $fullDesc.addClass('d-none');
      } else {
        $shortDesc.addClass('d-none');
        $fullDesc.removeClass('d-none');
      }
    };
  });