USE mydb;

SELECT J.Titulo, COUNT(G.id_Genero) AS NumeroDeGeneros
FROM Jogo J
JOIN Jogo_Genero JG ON J.idJogo = JG.Jogo_idJogo
JOIN Genero G ON JG.Genero_id_Genero = G.id_Genero
WHERE J.Gratuito = TRUE
GROUP BY J.Titulo;

SELECT J.Titulo, J.Preco, J.Data_Lancamento
FROM Jogo J
JOIN Usuario U ON J.Empresa_Usuario_id_Usuario = U.id_Usuario
WHERE U.Nome = 'EmpresaTeste';

SELECT U.Nome AS Empresa, COUNT(J.idJogo) AS NumeroDeJogos
FROM Usuario U
JOIN Jogo J ON U.id_Usuario = J.Empresa_Usuario_id_Usuario
WHERE U.Tipo = 'Empresa'
GROUP BY U.Nome;

SELECT J.Titulo, G.Nome AS Genero
FROM Jogo J
JOIN Jogo_Genero JG ON J.idJogo = JG.Jogo_idJogo
JOIN Genero G ON JG.Genero_id_Genero = G.id_Genero;

UPDATE Jogo
SET Preco = 69.99
WHERE idJogo= <IDJOGO>;

SELECT Titulo, Data_Lancamento
FROM Jogo
WHERE Data_Lancamento > '2023-01-01';

SELECT 
    A.Nota,
    A.Comentario,
    U.Nome AS NomeUsuario
FROM Avaliacao A
JOIN Usuario U ON A.Usuario_id_Usuario = U.id_Usuario  -- Junção com a tabela de usuários para pegar o nome
WHERE A.Jogo_idJogo = ID_JOGO  -- Substitua pelo id do jogo desejado
ORDER BY A.Nota DESC;  -- Ordena pela nota, com as melhores avaliações primeiro



