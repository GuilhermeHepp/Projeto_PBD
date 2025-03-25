USE mydb;

INSERT INTO usuario	(nome, tipo, email, senha) VALUES 
('teste_jogador_projeto', 'jogador', 'testejogador@gmail.com', '123'),
('teste_empresa_projeto', 'empresa', 'testeempresa@gmail.com', '1234');

INSERT INTO jogo (Titulo, Descricao, Gratuito, Requisitos, Preco, Data_Lancamento, Empresa_Usuario_id_Usuario) VALUES
('Jogo Ação 1', 'Descrição do Jogo Ação 1', FALSE, 'Requisitos 1', 59.99, '2023-05-10', ID_EMPRESA),
('Jogo Aventura 1', 'Descrição do Jogo Aventura 1', TRUE, 'Requisitos 2', 0.00, '2023-07-15',ID_EMPRESA);

INSERT INTO jogo_genero (Jogo_idJogo, Genero_id_Genero) VALUES
(1, 1),  -- Jogo Ação 1 é de Ação
(1, 2),  -- Jogo Ação 1 também é de Aventura
(2, 3);  -- Jogo Aventura 1 é de RPG 

INSERT INTO genero(nome) VALUES
('online'),
('cartas'),
('corrida');

INSERT INTO Avaliacao (Usuario_id_Usuario, Jogo_idJogo, Nota, Comentario) 
VALUES (ID_USUARIO, ID_JOGO, 4, 'Ótimo jogo, gostei muito dos gráficos e da jogabilidade!');

