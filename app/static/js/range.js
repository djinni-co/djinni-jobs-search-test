$(document).ready(function() {
    var $salaryRange = $('#salaryRange');
    var $salaryValue = $('#salaryValue');

    $salaryRange.on('input', function() {
      $salaryValue.text($salaryRange.val());
    });
  });