-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS mydb DEFAULT CHARACTER SET utf8mb3 ;
USE mydb ;

-- -----------------------------------------------------
-- Table mydb.usuario
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS mydb.usuario (
  id_Usuario INT NOT NULL AUTO_INCREMENT,
  Nome VARCHAR(100) NOT NULL,
  Email VARCHAR(100) NOT NULL,
  Senha VARCHAR(100) NOT NULL,
  Data_criacao DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  Tipo ENUM('Jogador', 'Empresa') NOT NULL,
  PRIMARY KEY (id_Usuario),
  UNIQUE INDEX Email (Email ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 147
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table mydb.jogador
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS mydb.jogador (
  Usuario_id_Usuario INT NOT NULL,
  CPF VARCHAR(14) NOT NULL,
  Saldo_Carteira DECIMAL(10,2) NULL DEFAULT '0.00',
  Data_Nascimento DATE NOT NULL,
  PRIMARY KEY (Usuario_id_Usuario),
  UNIQUE INDEX CPF (CPF ASC) VISIBLE,
  CONSTRAINT jogador_ibfk_1
    FOREIGN KEY (Usuario_id_Usuario)
    REFERENCES mydb.usuario (id_Usuario)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table mydb.empresa
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS mydb.empresa (
  Usuario_id_Usuario INT NOT NULL,
  CNPJ VARCHAR(20) NOT NULL,
  PRIMARY KEY (Usuario_id_Usuario),
  UNIQUE INDEX CNPJ (CNPJ ASC) VISIBLE,
  CONSTRAINT empresa_ibfk_1
    FOREIGN KEY (Usuario_id_Usuario)
    REFERENCES mydb.usuario (id_Usuario)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table mydb.jogo
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS mydb.jogo (
  idJogo INT NOT NULL AUTO_INCREMENT,
  Titulo VARCHAR(100) NOT NULL,
  Descricao TEXT NULL DEFAULT NULL,
  Preco DECIMAL(10,2) NOT NULL DEFAULT '0.00',
  Gratuito TINYINT(1) NULL DEFAULT '0',
  Data_Lancamento DATE NOT NULL,
  Requisitos VARCHAR(255) NULL DEFAULT NULL,
  Empresa_Usuario_id_Usuario INT NOT NULL,
  PRIMARY KEY (idJogo),
  INDEX Empresa_Usuario_id_Usuario (Empresa_Usuario_id_Usuario ASC) VISIBLE,
  CONSTRAINT jogo_ibfk_1
    FOREIGN KEY (Empresa_Usuario_id_Usuario)
    REFERENCES mydb.empresa (Usuario_id_Usuario)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
AUTO_INCREMENT = 6
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table mydb.avaliacao
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS mydb.avaliacao (
  idAvaliacao INT NOT NULL AUTO_INCREMENT,
  Usuario_id_Usuario INT NOT NULL,
  Jogo_idJogo INT NOT NULL,
  Nota INT NULL DEFAULT NULL,
  Comentario TEXT NULL DEFAULT NULL,
  PRIMARY KEY (idAvaliacao),
  INDEX Usuario_id_Usuario (Usuario_id_Usuario ASC) VISIBLE,
  INDEX Jogo_idJogo (Jogo_idJogo ASC) VISIBLE,
  CONSTRAINT avaliacao_ibfk_1
    FOREIGN KEY (Usuario_id_Usuario)
    REFERENCES mydb.jogador (Usuario_id_Usuario)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT avaliacao_ibfk_2
    FOREIGN KEY (Jogo_idJogo)
    REFERENCES mydb.jogo (idJogo)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table mydb.biblioteca
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS mydb.biblioteca (
  Usuario_id_Usuario INT NOT NULL,
  Jogo_id_Jogo INT NOT NULL,
  Data_Aquisicao DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (Usuario_id_Usuario, Jogo_id_Jogo),
  INDEX Jogo_idJogo (Jogo_id_Jogo ASC) VISIBLE,
  CONSTRAINT biblioteca_ibfk_1
    FOREIGN KEY (Usuario_id_Usuario)
    REFERENCES mydb.jogador (Usuario_id_Usuario)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT biblioteca_ibfk_2
    FOREIGN KEY (Jogo_id_Jogo)
    REFERENCES mydb.jogo (idJogo)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table mydb.genero
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS mydb.genero (
  id_Genero INT NOT NULL AUTO_INCREMENT,
  Nome VARCHAR(45) NOT NULL,
  PRIMARY KEY (id_Genero),
  UNIQUE INDEX Nome (Nome ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table mydb.jogo_genero
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS mydb.jogo_genero (
  Jogo_idJogo INT NOT NULL,
  Genero_id_Genero INT NOT NULL,
  PRIMARY KEY (Jogo_idJogo, Genero_id_Genero),
  INDEX Genero_id_Genero (Genero_id_Genero ASC) VISIBLE,
  CONSTRAINT jogo_genero_ibfk_1
    FOREIGN KEY (Jogo_idJogo)
    REFERENCES mydb.jogo (idJogo)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT jogo_genero_ibfk_2
    FOREIGN KEY (Genero_id_Genero)
    REFERENCES mydb.genero (id_Genero)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table mydb.pagamento
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS mydb.pagamento (
  Valor_Pago DECIMAL(10,2) NOT NULL,
  Forma_Pagamento VARCHAR(50) NOT NULL,
  Data_Pagamento DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  jogo_idJogo INT NOT NULL,
  jogador_Usuario_id_Usuario INT NOT NULL,
  PRIMARY KEY (jogo_idJogo, jogador_Usuario_id_Usuario),
  INDEX fk_pagamento_jogador1_idx (jogador_Usuario_id_Usuario ASC) VISIBLE,
  CONSTRAINT fk_pagamento_jogo1
    FOREIGN KEY (jogo_idJogo)
    REFERENCES mydb.jogo (idJogo)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT fk_pagamento_jogador1
    FOREIGN KEY (jogador_Usuario_id_Usuario)
    REFERENCES mydb.jogador (Usuario_id_Usuario)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;