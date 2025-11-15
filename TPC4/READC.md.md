# RELATORIO TPC4
## Aplicação de manutenção do cinema

### Descrição
**A aplicação tem como objetivo gerir as salas de cinema de um centro comercial. Cada sala pode ou não estar a exibir um filme e tem um número máximo de lugares disponíveis. Além disso, permite gerir os lugares ocupados e realizar várias operações de gestão relacionadas com as salas.**

#### Estrutura dos Dados
As salas de cinema são representadas por uma estrutura organizada que mantém a informação essencial sobre cada sala, incluindo:

Número de lugares: A capacidade total da sala.
Lugares vendidos: A lista dos lugares que já foram ocupados por clientes, identificados por números inteiros.
Filme em exibição: O nome do filme que está atualmente a ser exibido na sala.

##### Como a Aplicação Funciona
A aplicação utiliza esta estrutura para organizar e gerir as salas de cinema. O utilizador pode interagir com a aplicação através de um menu interativo que oferece várias opções de operações. O fluxo típico de interação com a aplicação é o seguinte:

Inserir Salas: O utilizador pode adicionar novas salas ao cinema. Cada sala tem uma lotação definida, e o utilizador também define qual filme está a ser exibido nessa sala. Antes de adicionar uma nova sala, a aplicação verifica se já existe uma sala exibindo o mesmo filme para evitar duplicação.

Vender Bilhetes: Através do menu, o utilizador pode vender bilhetes para um determinado filme. A aplicação verifica se o lugar especificado está disponível antes de confirmar a venda. Se o lugar já estiver ocupado, a venda é rejeitada.

Verificar Disponibilidade de Lugares: O utilizador pode verificar se um determinado lugar está disponível para um filme em exibição. Isso é útil antes de tentar vender bilhetes, ou para fornecer informações aos clientes sobre a ocupação da sala.

Listar Filmes e Disponibilidade: A aplicação permite listar todos os filmes que estão em exibição no momento. Além disso, é possível consultar quantos lugares estão disponíveis em cada sala de cinema, facilitando o controle e a gestão das salas.



 