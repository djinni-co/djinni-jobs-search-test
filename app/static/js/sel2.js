$(document).ready(function() {
    function initializeSelect2(id) {
      $('#' + id).select2({
        theme: 'bootstrap-5'
      });
    }

    initializeSelect2('id_remote_type');
    initializeSelect2('id_relocate_type');
    initializeSelect2('id_accept_region');
    initializeSelect2('id_english_level');
    initializeSelect2('id_domain');
    initializeSelect2('id_company_type');
    initializeSelect2('id_experience_years');
    initializeSelect2('id_position');
    initializeSelect2('id_location');
    initializeSelect2('id_country');
  });