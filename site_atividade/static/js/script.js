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

$(document).ready(function() {
  // Botão de adicionar quantidade
  $(".btn-add-quantity").click(function() {
    var quantidadeElement = $(this).closest("tr").find(".quantidade");

    // Obtém a quantidade atual do produto
    var quantidadeAtual = parseInt(quantidadeElement.text());

    // Incrementa a quantidade
    quantidadeAtual++;

    // Atualiza o valor exibido na tabela
    quantidadeElement.text(quantidadeAtual);
  });

  // Botão de remover quantidade
  $(".btn-remove-quantity").click(function() {
    var quantidadeElement = $(this).closest("tr").find(".quantidade");

    // Obtém a quantidade atual do produto
    var quantidadeAtual = parseInt(quantidadeElement.text());

    // Verifica se a quantidade atual é maior que zero antes de decrementar
    if (quantidadeAtual > 0) {
      // Decrementa a quantidade
      quantidadeAtual--;

      // Atualiza o valor exibido na tabela
      quantidadeElement.text(quantidadeAtual);
    }
  });

  // Botão de adicionar à venda
// Botão de adicionar à venda
  $(document).on('click', '.btn-add-venda', function() {
    var produtoId = $(this).data('produto-id');
    var quantidade = parseInt($(this).siblings('.quantidade').text());

    if (quantidade === 0) {
      // Exibe uma flash message informando que a quantidade não pode ser zero
      var flashMessage = $('<div class="flash-message">A quantidade não pode ser zero.</div>');
      $('body').append(flashMessage);
      setTimeout(function() {
        flashMessage.remove();
      }, 3000); // Remove a flash message após 3 segundos
      return;
    }

    $.post('/adicionar_venda', {produto_id: produtoId, quantidade: quantidade}, function(data) {
      if (data.success) {
        // Atualiza o conteúdo da variável vendas_html
        var vendas_html = data.vendas_html;

        // Substitui todo o corpo da tabela de vendas com o novo conteúdo
        $('.table-vendas tbody').html(vendas_html);
      } else {
        // Exiba uma mensagem de erro, se necessário
        var flashMessage = $('<div class="flash-message">' + data.message + '</div>');
        $('body').append(flashMessage);
        setTimeout(function() {
          flashMessage.remove();
        }, 3000); // Remove a flash message após 3 segundos
      }
    }, 'json');
  });

});






