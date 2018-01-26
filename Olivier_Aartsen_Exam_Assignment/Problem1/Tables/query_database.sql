--By:			Olivier Aartsen
--Studentnumber:	s1397478
--Last modified on:	26/01/2018
--This file will query through the database giving the results asked for in problem 1b) (so for R1, R2, R3, R4 and R5)
.open prob1.db
.headers on
.mode list

.print "Before I begin querying, let me explain the structure of the database (note that this is not the justification just an explanation). So every fits file with the same filter has been unified into a new table called exactly that filter, for example the fits files that contain the H-filter (Field-1-H.fits, Field-2-H.fits and Field-3-H.fits) are unified into one table called H. This is done so that the StarID remains unique in each table. Now for the Ks filter this is more complicated since there are multiple exposures of one filter in a field, so I unified these into new tables based upon the order in which they were taken. So for example the fits files Field-1-Ks-E002.fits and Field-3-Ks-E002.fits have been unified into a new table called Ks2. Furthermore I have added the columns ExpID and Field to the new data-tables, the ExpID stands for exposure index and is a unique index for each exposure (so since we have 18 fits files there are 18 unique exposures and therefore ExpID ranges from 1 to 18). Field is just the field in which it was taken. Finally the Info table contains the information about each exposure where the ID in this table relates directly to the ExpID in the data-tables. I have also added one column; Tablename containing a easy to understand description of the exposure: for example F1Z stands for Field 1 and Z stands for the Z-filter (so it is the exposure taken in field 1 in the Z-filter). Now the final example is that of F1KsE002 which has the same structure as explained for F1Z (so Field 1 and Ks-filter) but now it also has E002 which means the second image taken in field 1 in the Ks-filter."
--For more clarity add a new-line:
.print " "

--R1:
.print "R1:"
.print "So below is a list of the amount of stars with S/N > 5 in each image taken between MJD=56800 and MJD=57300:"

SELECT u.ExpID, COUNT(u.StarID) as nStars, i.Tablename AS Image FROM (SELECT * FROM H UNION SELECT * FROM J UNION SELECT * FROM Ks1 UNION SELECT * FROM Ks2 UNION SELECT * FROM Ks3 UNION SELECT * FROM Y UNION SELECT * FROM Z) AS u JOIN Info as i ON u.ExpID = i.ID WHERE i.MJD BETWEEN 56800 AND 57300 AND u.Flux1/u.dFlux1 > 5 GROUP BY u.ExpID;


.print " "
--R2:
.print "R2:"
.print "Here are the objects that have J-H > 1.5 (I limit the output to 5 to avoid filling the terminal): "
SELECT H.StarID, ROUND(J.Mag1-H.Mag1, 2) as JH FROM H JOIN J on H.starID = J.StarID WHERE J.Mag1 - H.Mag1 > 1.5 LIMIT 5;

.print " "

--R3
.print "R3:"
.print "Here are the objects in field 1 where any of the measurements of the flux in the Ks-filter is more than 20 times the uncertainty of that flux away from the average flux of that object in the Ks-filter (limited to 5 outputs):"
SELECT Ks1.StarID, ROUND((Ks1.Flux1 + Ks2.Flux1 + Ks3.Flux1)/3, 2) as AverageFlux, ROUND(Ks1.Flux1, 2) as Ks1Flux, ROUND(Ks1.dFlux1, 2) as Ks1Fluxerr, ROUND(Ks2.Flux1, 2) as Ks2Flux, ROUND(Ks2.dFlux1, 2) as Ks2Fluxerr, ROUND(Ks3.Flux1, 2) as Ks3Flux, ROUND(Ks3.dFlux1, 2) as Ks3Fluxerr FROM Ks1 JOIN Ks2 ON Ks1.StarID = Ks2.StarID JOIN Ks3 ON Ks1.StarID = Ks3.StarID WHERE (abs(Ks1.Flux1 - AverageFlux) > 20*Ks1.dFlux1 OR abs(Ks2.Flux1 - AverageFlux) > 20*Ks2.dFlux1 OR abs(Ks3.Flux1 - AverageFlux) > 20*Ks3.dFlux1) AND Ks1.Field = 1 LIMIT 5;

.print " "

.print "For field 2 this query does not make any sense since it only has one exposure in the Ks-filter. Therefore there is nothing to compare this exposure to."

.print " "

.print "For field 3 there are 2 measurements of the flux in the Ks-filter, therefore we can perform this query. So here are the objects in field 3 where any of the two measurements of the flux in the Ks-filter is more than 20 times the uncertainty of that flux away from the average flux of that object in the Ks-filter (limited to 5 outputs):"
SELECT Ks1.StarID, ROUND((Ks1.Flux1 + Ks2.Flux1)/2, 2) as AverageFlux, ROUND(Ks1.Flux1, 2) as Ks1Flux, ROUND(Ks1.dFlux1, 2) as Ks1Fluxerr, ROUND(Ks2.Flux1, 2) as Ks2Flux, ROUND(Ks2.dFlux1, 2) as Ks2Fluxerr FROM Ks1 JOIN Ks2 ON Ks1.StarID = Ks2.StarID WHERE (abs(Ks1.Flux1 - AverageFlux) > 20*Ks1.dFlux1 OR abs(Ks2.Flux1 - AverageFlux) > 20*Ks2.dFlux1) AND Ks1.Field = 3 LIMIT 5;


.print " "
--R4
.print "R4:"
.print "The following catalogues exist for field 1:"
SELECT Tablename FROM Info WHERE FieldID = 1;

.print "The following catalogues exist for field 2:"
SELECT Tablename FROM Info WHERE FieldID = 2;

.print "The following catalogues exist for field 3:"
SELECT Tablename FROM Info WHERE FieldID = 3;


.print " "
--R5
.print "R5:"
--Note that the commands for different fields is easily changed by just changing Y.Field=1 to Y.Field=2 (or 3) (so everything is the same in the commands for different fields except for Y.Field). An important thing to keep in mind is that some fields will not have the Ks2 or Ks3 filters so these columns will just be empty

.print "The following stars have S/N > 30 for all filters in Field 1 (limited to 5 outputs):"
SELECT Y.StarID, ROUND(Y.Mag1, 1) AS MagY, ROUND(Y.Flux1 / Y.dFlux1, 2) as SNY, ROUND(Z.Mag1, 1) AS MagZ, ROUND(Z.Flux1 / Z.dFlux1, 2) as SNZ, ROUND(J.Mag1, 1) AS MagJ, ROUND(J.Flux1 / J.dFlux1, 2) as SNJ, ROUND(H.Mag1, 1) AS MagH, ROUND(H.Flux1 / H.dFlux1, 2) as SNH, ROUND(Ks1.Mag1, 1) AS MagKs1, ROUND(Ks1.Flux1 / Ks1.dFlux1, 2) as SNKs1, ROUND(Ks2.Mag1, 1) AS MagKs2, ROUND(Ks2.Flux1 / Ks2.dFlux1, 2) as SNKs2, ROUND(Ks3.Mag1, 1) AS MagKs3, ROUND(Ks3.Flux1 / Ks3.dFlux1, 2) as SNKs3 FROM Y LEFT OUTER JOIN Z ON Y.StarID = Z.StarID LEFT OUTER JOIN J ON Y.StarID = J.StarID LEFT OUTER JOIN H ON Y.StarID = H.StarID LEFT OUTER JOIN Ks1 ON Y.StarID = Ks1.StarID LEFT OUTER JOIN Ks2 ON Y.StarID = Ks2.StarID LEFT OUTER JOIN Ks3 ON Y.StarID = Ks3.StarID WHERE SNY > 30 AND Z.Flux1 / Z.dFlux1 > 30 AND J.Flux1 / J.dFlux1 > 30 AND H.Flux1 / H.dFlux1 > 30 AND Ks1.Flux1 / Ks1.dFlux1 > 30 AND (Ks2.Flux1 / Ks2.dFlux1 > 30 OR Ks2.Flux1 is NULL) AND (Ks3.Flux1 / Ks3.dFlux1 > 30 OR Ks3.Flux1 is NULL) AND Y.Class = -1 AND Y.Field=1 LIMIT 5;

.print " "
.print "The following stars have S/N > 30 for all filters in Field 2 (since Ks2 and Ks3 do not exist in this field the magnitudes in these filters will be empty, also limited to 5 outputs):
SELECT Y.StarID, ROUND(Y.Mag1, 1) AS MagY, ROUND(Y.Flux1 / Y.dFlux1, 2) as SNY, ROUND(Z.Mag1, 1) AS MagZ, ROUND(Z.Flux1 / Z.dFlux1, 2) as SNZ, ROUND(J.Mag1, 1) AS MagJ, ROUND(J.Flux1 / J.dFlux1, 2) as SNJ, ROUND(H.Mag1, 1) AS MagH, ROUND(H.Flux1 / H.dFlux1, 2) as SNH, ROUND(Ks1.Mag1, 1) AS MagKs1, ROUND(Ks1.Flux1 / Ks1.dFlux1, 2) as SNKs1, ROUND(Ks2.Mag1, 1) AS MagKs2, ROUND(Ks2.Flux1 / Ks2.dFlux1, 2) as SNKs2, ROUND(Ks3.Mag1, 1) AS MagKs3, ROUND(Ks3.Flux1 / Ks3.dFlux1, 2) as SNKs3 FROM Y LEFT OUTER JOIN Z ON Y.StarID = Z.StarID LEFT OUTER JOIN J ON Y.StarID = J.StarID LEFT OUTER JOIN H ON Y.StarID = H.StarID LEFT OUTER JOIN Ks1 ON Y.StarID = Ks1.StarID LEFT OUTER JOIN Ks2 ON Y.StarID = Ks2.StarID LEFT OUTER JOIN Ks3 ON Y.StarID = Ks3.StarID WHERE SNY > 30 AND Z.Flux1 / Z.dFlux1 > 30 AND J.Flux1 / J.dFlux1 > 30 AND H.Flux1 / H.dFlux1 > 30 AND Ks1.Flux1 / Ks1.dFlux1 > 30 AND (Ks2.Flux1 / Ks2.dFlux1 > 30 OR Ks2.Flux1 is NULL) AND (Ks3.Flux1 / Ks3.dFlux1 > 30 OR Ks3.Flux1 is NULL) AND Y.Class = -1 AND Y.Field=2 LIMIT 5;

.print " "
.print "The following stars have S/N > 30 for all filters in Field 3 (since Ks3 does not exist in this field the magnitudes in this filter will be empty, also limited to 5 outputs):"
SELECT Y.StarID, ROUND(Y.Mag1, 1) AS MagY, ROUND(Y.Flux1 / Y.dFlux1, 2) as SNY, ROUND(Z.Mag1, 1) AS MagZ, ROUND(Z.Flux1 / Z.dFlux1, 2) as SNZ, ROUND(J.Mag1, 1) AS MagJ, ROUND(J.Flux1 / J.dFlux1, 2) as SNJ, ROUND(H.Mag1, 1) AS MagH, ROUND(H.Flux1 / H.dFlux1, 2) as SNH, ROUND(Ks1.Mag1, 1) AS MagKs1, ROUND(Ks1.Flux1 / Ks1.dFlux1, 2) as SNKs1, ROUND(Ks2.Mag1, 1) AS MagKs2, ROUND(Ks2.Flux1 / Ks2.dFlux1, 2) as SNKs2, ROUND(Ks3.Mag1, 1) AS MagKs3, ROUND(Ks3.Flux1 / Ks3.dFlux1, 2) as SNKs3 FROM Y LEFT OUTER JOIN Z ON Y.StarID = Z.StarID LEFT OUTER JOIN J ON Y.StarID = J.StarID LEFT OUTER JOIN H ON Y.StarID = H.StarID LEFT OUTER JOIN Ks1 ON Y.StarID = Ks1.StarID LEFT OUTER JOIN Ks2 ON Y.StarID = Ks2.StarID LEFT OUTER JOIN Ks3 ON Y.StarID = Ks3.StarID WHERE SNY > 30 AND Z.Flux1 / Z.dFlux1 > 30 AND J.Flux1 / J.dFlux1 > 30 AND H.Flux1 / H.dFlux1 > 30 AND Ks1.Flux1 / Ks1.dFlux1 > 30 AND (Ks2.Flux1 / Ks2.dFlux1 > 30 OR Ks2.Flux1 is NULL) AND (Ks3.Flux1 / Ks3.dFlux1 > 30 OR Ks3.Flux1 is NULL) AND Y.Class = -1 AND Y.Field=3 LIMIT 5;


--IMPORTANT:
--For R2, R3 and R5 the output was more than 20 entries long (if I wouldn't have put the LIMIT on), so I dumped these outputs to a few files. Here is an commented example of what I did for R2 (just by opening the database in sqlite3 and then entering the following commands):
--.mode csv
--.headers on
--.out JH1_5.csv 
--SELECT H.StarID, ROUND(J.Mag1-H.Mag1, 2) as JH FROM H JOIN J on H.starID = J.StarID WHERE J.Mag1 - H.Mag1 > 1.5 AND JH IS NOT NULL;
--.exit
--THE DUMP FILE COMMANDS ARE LOCATED IN dump_tables.sql
