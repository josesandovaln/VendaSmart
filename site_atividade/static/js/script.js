$(document).ready(function() {
    $('#search-input').on('input', function() {
        var searchTerm = $(this).val().toLowerCase();
        filterTable(searchTerm);
    });

    function filterTable(searchTerm) {
        $('.list-product tbody tr').each(function() {
            var $row = $(this);

            if ($row.text().toLowerCase().indexOf(searchTerm) === -1) {
                $row.hide();
            } else {
                $row.show();
            }
        });
    }
});

$(document).ready(function() {
    $('#search-input').on('input', function() {
      var searchTerm = $(this).val().toLowerCase();
      filterTable(searchTerm);
    });
  
    function filterTable(searchTerm) {
      $('.table tbody tr').each(function() {
        var $row = $(this);
  
        if ($row.text().toLowerCase().indexOf(searchTerm) === -1) {
          $row.hide();
        } else {
          $row.show();
        }
      });
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const excluirUsuarioModal = document.getElementById('excluirUsuarioModal');
    const usuarioNomeElement = excluirUsuarioModal.querySelector('#usuarioNome');
    const excluirUsuarioBtn = excluirUsuarioModal.querySelector('#excluirUsuarioBtn');

    const excluirUsuarioBtns = document.getElementsByClassName('excluir-usuario-btn');

    for (let i = 0; i < excluirUsuarioBtns.length; i++) {
        excluirUsuarioBtns[i].addEventListener('click', function(event) {
            event.preventDefault();

            const href = this.getAttribute('data-href');
            const usuarioNome = this.parentNode.parentNode.querySelector('td:nth-child(2)').textContent;

            usuarioNomeElement.textContent = usuarioNome;
            excluirUsuarioBtn.setAttribute('href', href);

            excluirUsuarioModal.modal('show');
        });
    }
});