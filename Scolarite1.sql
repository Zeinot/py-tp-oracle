CREATE TABLE Etudiant (
    IdEt VARCHAR2(10) PRIMARY KEY,
    NomEt VARCHAR2(255),
    PrenomEt VARCHAR2(255),
    DateNais DATE
);
CREATE SEQUENCE etudiant_seq
  MINVALUE 1
  MAXVALUE 999999999999999999999999999
  START WITH 1
  INCREMENT BY 1
  CACHE 20;

CREATE OR REPLACE TRIGGER trg_etudiant_id
BEFORE INSERT ON Etudiant
FOR EACH ROW
BEGIN
  :NEW.IdEt := 'ET' || LPAD(etudiant_seq.NEXTVAL, 4, '0');
END;
/

-- Insert data into the Etudiant table
INSERT INTO Etudiant (NomEt, PrenomEt, DateNais) 
    VALUES ('Dupont', 'Jean', TO_DATE('1995-04-15', 'YYYY-MM-DD'));
INSERT INTO Etudiant (NomEt, PrenomEt, DateNais) 
    VALUES ('Martin', 'Alice', TO_DATE('1997-08-21', 'YYYY-MM-DD'));
INSERT INTO Etudiant (NomEt, PrenomEt, DateNais) 
    VALUES ('Durand', 'Sophie', TO_DATE('1999-12-30', 'YYYY-MM-DD'));

-- Check the inserted data
SELECT * FROM Etudiant;

