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

    // Atualiza o valor do estoque
    var estoqueElement = $(this).closest("tr").find(".estoque");
    var estoqueAtual = parseInt(estoqueElement.text());
    estoqueElement.text(estoqueAtual - 1);
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

    // Atualiza o valor do estoque
    var estoqueElement = $(this).closest("tr").find(".estoque");
    var estoqueAtual = parseInt(estoqueElement.text());
    estoqueElement.text(estoqueAtual + 1);


  });

    // Selecionar cliente
    $('.btn-selecionar-cliente').one('click', function(event) {
        event.preventDefault(); // Impede o comportamento padrão de envio do formulário
        console.log('Clique no botão "selecionar cliente"');
        var clienteId = $('#cliente_id').val();
    
        $.ajax({
            url: '/adicionar_venda',
            method: 'POST',
            data: { cliente_id: clienteId },
            success: function(response) {
                console.log('Resposta do servidor:', response);
                if (response.success) {
                    $('.btn-selecionar-cliente').attr('disabled', true);
                    $('.btn-adicionar-venda').attr('disabled', false);
                    alert('Cliente selecionado com sucesso.');
                } else {
                    alert(response.message);
                }
            },
            error: function() {
                console.log('Erro ao processar a solicitação.');
                alert('Ocorreu um erro ao processar a solicitação.');
            }
        });
    });
    
    



  // Adicionar à venda
  $(document).on('click', '.btn-add-venda', function() {
    var produtoId = $(this).data('produto-id');
    var quantidade = parseInt($(this).siblings('.quantidade').text());

    if (quantidade === 0) {
      var flashMessage = $('<div class="flash-message">A quantidade não pode ser zero.</div>');
      $('body').append(flashMessage);
      setTimeout(function() {
        flashMessage.remove();
      }, 3000);
      return;
    }

    $.post('/adicionar_item_venda', {produto_id: produtoId, quantidade: quantidade}, function(data) {
        if (data.success) {
          // Atualiza o conteúdo da variável vendas_html
          vendas_html = data.vendas_html;
  
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
    // Requisição AJAX para obter as informações do último pagamento
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/obter_ultimo_pagamento');
    xhr.onload = function () {
        if (xhr.status === 200) {
            var ultimoPagamento = JSON.parse(xhr.responseText).ultimo_pagamento;

            // Obtém as informações do último pagamento
            var metodoPagamento = ultimoPagamento.metodo_pagamento;
            var valorPagamento = ultimoPagamento.valor_pagamento;
            var troco = ultimoPagamento.troco;
            var valorTotalVendas = ultimoPagamento.valor_total_vendas;  // Obtém o valor total das vendas

            // Cria a mensagem com as informações do pagamento
            var mensagem = 'Dados do pagamento:\n';
            mensagem += 'Método de pagamento: ' + metodoPagamento + '\n';
            mensagem += 'Valor do pagamento: R$ ' + valorPagamento + '\n';
            mensagem += 'Troco: R$ ' + troco + '\n';
            mensagem += 'Valor total da compra: R$ ' + valorTotalVendas + '\n';  // Adiciona o valor total das vendas
            mensagem += 'Data do pagamento: ' + ultimoPagamento.data_pagamento;

            // Redireciona para o WhatsApp com a mensagem preenchida
            window.location.href = 'https://api.whatsapp.com/send?text=' + encodeURIComponent(mensagem);
        }
    };
    xhr.send();
  });
  

  enviarEmailBtn.addEventListener('click', function () {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/obter_ultimo_pagamento');
    xhr.onload = function () {
        if (xhr.status === 200) {
            var ultimoPagamento = JSON.parse(xhr.responseText).ultimo_pagamento;

            var metodoPagamento = ultimoPagamento.metodo_pagamento;
            var valorPagamento = ultimoPagamento.valor_pagamento;
            var troco = ultimoPagamento.troco;
            var valorTotalVendas = ultimoPagamento.valor_total_vendas;
            var dataPagamento = ultimoPagamento.data_pagamento;

            var emailCorpo = 'Dados do pagamento:\n\n';
            emailCorpo += 'Método de pagamento: ' + metodoPagamento + '\n';
            emailCorpo += 'Valor do pagamento: R$ ' + valorPagamento + '\n';
            emailCorpo += 'Troco: R$ ' + troco + '\n';
            emailCorpo += 'Valor total da compra: R$ ' + valorTotalVendas + '\n';
            emailCorpo += 'Data do pagamento: ' + dataPagamento;

            window.location.href = 'mailto:?subject=Comprovante de Pagamento&body=' + encodeURIComponent(emailCorpo);
        }
    };
    xhr.send();
  });


  enviarComprovanteForm.addEventListener('submit', function (event) {
      // Prevent form submission
      event.preventDefault();
      // Show the modal
      $('#escolher-modal').modal('show');
  });
});


