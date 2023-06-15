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


//////////////////////////    CARTÃO DE CREDITO    ///////////////////////////////////
$(document).ready(function() {
  // Oculta o campo de seleção de parcelas inicialmente
  $('#parcelas-field').hide();

  // Mostra ou oculta o campo de seleção de parcelas com base na seleção do método de pagamento
  $('#metodo_pagamento').change(function() {
      if ($(this).val() === 'cartao_de_credito') {
          $('#parcelas-field').show();
      } else {
          $('#parcelas-field').hide();
      }
  });
});
//////////////////////////    CARTÃO DE CREDITO    ///////////////////////////////////


// JavaScript code to handle modal button clicks and form submission
document.addEventListener('DOMContentLoaded', function () {
  var enviarWhatsappBtn = document.getElementById('enviar-whatsapp-btn');
  var enviarEmailBtn = document.getElementById('enviar-email-btn');
  var enviarComprovanteForm = document.getElementById('enviar-comprovante-form');

  enviarWhatsappBtn.addEventListener('click', function () {
      // Redirect to WhatsApp using the chosen data
      window.location.href = 'https://api.whatsapp.com/send?text=' + encodeURIComponent('Dados do pagamento: ...');
  });

  enviarEmailBtn.addEventListener('click', function () {
      // Open email client with pre-filled data
      window.location.href = 'mailto:?subject=Comprovante de Pagamento&body=Dados do pagamento: ...';
  });

  enviarComprovanteForm.addEventListener('submit', function (event) {
      // Prevent form submission
      event.preventDefault();
      // Show the modal
      $('#escolher-modal').modal('show');
  });
});

