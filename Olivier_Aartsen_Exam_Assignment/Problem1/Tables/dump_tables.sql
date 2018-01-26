--By: 			Olivier Aartsen
--Studentnumber:	s1397478
--Last modified on:	26/01/2018
--This file is meant to dump the tables of queries R2, R3 and R5 so that these results can be plotted graphically.

--Open the database and config the mode and headers:
.open prob1.db
.mode csv
.headers on

--For R2:
.out JH1_5.csv 
SELECT H.StarID, ROUND(J.Mag1-H.Mag1, 3) as JH FROM H JOIN J on H.starID = J.StarID WHERE J.Mag1 - H.Mag1 > 1.5 AND JH IS NOT NULL;

--For R3 the following 2 dumps:
.out R3_F1.csv
SELECT Ks1.StarID, ROUND((Ks1.Flux1 + Ks2.Flux1 + Ks3.Flux1)/3, 2) as AverageFlux, ROUND(Ks1.Flux1, 2) as Ks1Flux, ROUND(Ks1.dFlux1, 2) as Ks1Fluxerr, ROUND(Ks2.Flux1, 2) as Ks2Flux, ROUND(Ks2.dFlux1, 2) as Ks2Fluxerr, ROUND(Ks3.Flux1, 2) as Ks3Flux, ROUND(Ks3.dFlux1, 2) as Ks3Fluxerr FROM Ks1 JOIN Ks2 ON Ks1.StarID = Ks2.StarID JOIN Ks3 ON Ks1.StarID = Ks3.StarID WHERE (abs(Ks1.Flux1 - AverageFlux) > 20*Ks1.dFlux1 OR abs(Ks2.Flux1 - AverageFlux) > 20*Ks2.dFlux1 OR abs(Ks3.Flux1 - AverageFlux) > 20*Ks3.dFlux1) AND Ks1.Field = 1;

.out R3_F3.csv
SELECT Ks1.StarID, ROUND((Ks1.Flux1 + Ks2.Flux1)/2, 2) as AverageFlux, ROUND(Ks1.Flux1, 2) as Ks1Flux, ROUND(Ks1.dFlux1, 2) as Ks1Fluxerr, ROUND(Ks2.Flux1, 2) as Ks2Flux, ROUND(Ks2.dFlux1, 2) as Ks2Fluxerr FROM Ks1 JOIN Ks2 ON Ks1.StarID = Ks2.StarID WHERE (abs(Ks1.Flux1 - AverageFlux) > 20*Ks1.dFlux1 OR abs(Ks2.Flux1 - AverageFlux) > 20*Ks2.dFlux1) AND Ks1.Field = 3;


--For R5:
.out SN30_F1.csv
SELECT Y.StarID, ROUND(Y.Mag1, 2) AS MagY, ROUND(Y.Flux1 / Y.dFlux1, 2) as SNY, ROUND(Z.Mag1, 2) AS MagZ, ROUND(Z.Flux1 / Z.dFlux1, 2) as SNZ, ROUND(J.Mag1, 2) AS MagJ, ROUND(J.Flux1 / J.dFlux1, 2) as SNJ, ROUND(H.Mag1, 2) AS MagH, ROUND(H.Flux1 / H.dFlux1, 2) as SNH, ROUND(Ks1.Mag1, 2) AS MagKs1, ROUND(Ks1.Flux1 / Ks1.dFlux1, 2) as SNKs1, ROUND(Ks2.Mag1, 2) AS MagKs2, ROUND(Ks2.Flux1 / Ks2.dFlux1, 2) as SNKs2, ROUND(Ks3.Mag1, 2) AS MagKs3, ROUND(Ks3.Flux1 / Ks3.dFlux1, 2) as SNKs3 FROM Y LEFT OUTER JOIN Z ON Y.StarID = Z.StarID LEFT OUTER JOIN J ON Y.StarID = J.StarID LEFT OUTER JOIN H ON Y.StarID = H.StarID LEFT OUTER JOIN Ks1 ON Y.StarID = Ks1.StarID LEFT OUTER JOIN Ks2 ON Y.StarID = Ks2.StarID LEFT OUTER JOIN Ks3 ON Y.StarID = Ks3.StarID WHERE SNY > 30 AND Z.Flux1 / Z.dFlux1 > 30 AND J.Flux1 / J.dFlux1 > 30 AND H.Flux1 / H.dFlux1 > 30 AND Ks1.Flux1 / Ks1.dFlux1 > 30 AND (Ks2.Flux1 / Ks2.dFlux1 > 30 OR Ks2.Flux1 is NULL) AND (Ks3.Flux1 / Ks3.dFlux1 > 30 OR Ks3.Flux1 is NULL) AND Y.Class = -1 AND Y.Field=1;

.out SN30_F2.csv
SELECT Y.StarID, ROUND(Y.Mag1, 2) AS MagY, ROUND(Y.Flux1 / Y.dFlux1, 2) as SNY, ROUND(Z.Mag1, 2) AS MagZ, ROUND(Z.Flux1 / Z.dFlux1, 2) as SNZ, ROUND(J.Mag1, 2) AS MagJ, ROUND(J.Flux1 / J.dFlux1, 2) as SNJ, ROUND(H.Mag1, 2) AS MagH, ROUND(H.Flux1 / H.dFlux1, 2) as SNH, ROUND(Ks1.Mag1, 2) AS MagKs1, ROUND(Ks1.Flux1 / Ks1.dFlux1, 2) as SNKs1, ROUND(Ks2.Mag1, 2) AS MagKs2, ROUND(Ks2.Flux1 / Ks2.dFlux1, 2) as SNKs2, ROUND(Ks3.Mag1, 2) AS MagKs3, ROUND(Ks3.Flux1 / Ks3.dFlux1, 2) as SNKs3 FROM Y LEFT OUTER JOIN Z ON Y.StarID = Z.StarID LEFT OUTER JOIN J ON Y.StarID = J.StarID LEFT OUTER JOIN H ON Y.StarID = H.StarID LEFT OUTER JOIN Ks1 ON Y.StarID = Ks1.StarID LEFT OUTER JOIN Ks2 ON Y.StarID = Ks2.StarID LEFT OUTER JOIN Ks3 ON Y.StarID = Ks3.StarID WHERE SNY > 30 AND Z.Flux1 / Z.dFlux1 > 30 AND J.Flux1 / J.dFlux1 > 30 AND H.Flux1 / H.dFlux1 > 30 AND Ks1.Flux1 / Ks1.dFlux1 > 30 AND (Ks2.Flux1 / Ks2.dFlux1 > 30 OR Ks2.Flux1 is NULL) AND (Ks3.Flux1 / Ks3.dFlux1 > 30 OR Ks3.Flux1 is NULL) AND Y.Class = -1 AND Y.Field=2;

.out SN30_F3.csv
SELECT Y.StarID, ROUND(Y.Mag1, 2) AS MagY, ROUND(Y.Flux1 / Y.dFlux1, 2) as SNY, ROUND(Z.Mag1, 2) AS MagZ, ROUND(Z.Flux1 / Z.dFlux1, 2) as SNZ, ROUND(J.Mag1, 2) AS MagJ, ROUND(J.Flux1 / J.dFlux1, 2) as SNJ, ROUND(H.Mag1, 2) AS MagH, ROUND(H.Flux1 / H.dFlux1, 2) as SNH, ROUND(Ks1.Mag1, 2) AS MagKs1, ROUND(Ks1.Flux1 / Ks1.dFlux1, 2) as SNKs1, ROUND(Ks2.Mag1, 2) AS MagKs2, ROUND(Ks2.Flux1 / Ks2.dFlux1, 2) as SNKs2, ROUND(Ks3.Mag1, 2) AS MagKs3, ROUND(Ks3.Flux1 / Ks3.dFlux1, 2) as SNKs3 FROM Y LEFT OUTER JOIN Z ON Y.StarID = Z.StarID LEFT OUTER JOIN J ON Y.StarID = J.StarID LEFT OUTER JOIN H ON Y.StarID = H.StarID LEFT OUTER JOIN Ks1 ON Y.StarID = Ks1.StarID LEFT OUTER JOIN Ks2 ON Y.StarID = Ks2.StarID LEFT OUTER JOIN Ks3 ON Y.StarID = Ks3.StarID WHERE SNY > 30 AND Z.Flux1 / Z.dFlux1 > 30 AND J.Flux1 / J.dFlux1 > 30 AND H.Flux1 / H.dFlux1 > 30 AND Ks1.Flux1 / Ks1.dFlux1 > 30 AND (Ks2.Flux1 / Ks2.dFlux1 > 30 OR Ks2.Flux1 is NULL) AND (Ks3.Flux1 / Ks3.dFlux1 > 30 OR Ks3.Flux1 is NULL) AND Y.Class = -1 AND Y.Field=3;



--For Problem 1c)
.out JH_YJ.csv
SELECT H.StarID, ROUND(J.Mag1-H.Mag1, 2) as JH, ROUND(Y.Mag1-J.Mag1, 2) as YJ FROM H JOIN J on H.starID = J.StarID JOIN Y ON H.StarID = Y.StarID WHERE JH IS NOT NULL AND YJ IS NOT NULL AND H.Class = -1;
.exit
