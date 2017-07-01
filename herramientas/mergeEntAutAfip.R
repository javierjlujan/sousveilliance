
### Codigo para matchear/mergear bases de Autoridades, Entidades y AFIP
### en base campos de nombre.
### Genera una base que une las variables de todas las bases que se cargan
### Y agrega la informacion de CUIT a la empresa que no esta disponible
### en las bases de IGJ.
### Hecho por Sebastián Freille el 1 de Julio de 2017 .



### Carga Base Entidades IGJ
ent <- read.csv("igj-entidades.csv",header=TRUE)

ent <- ent[order(ent$razon_social),]
ent$razon_social <- gsub("[.]","",ent$razon_social,fixed=FALSE)
ent$razon_social <- gsub("[,]","",ent$razon_social,fixed=FALSE)

### Carga Base Autoridad IGJ
igj <- read.csv("igj-autoridades.csv",header=TRUE

                ### Para hacer un trimming de whitespace
                ### ent$razon_social <- trimws(ent$razon_social)


### Base Afip
### Carga Base Afip desde Mismo Directorio

afip <- read.csv("afip.txt",header=TRUE)


### Ordenar alfabeticamente por nombre
afip <- afip[order(afip$nombre),]

### Reemplazar caracteres extraños por espacios
afip$nombre <- gsub("\"","",afip$nombre)


### Matching/Merging

### Match/merge Entidad con AFIP
try <- merge(ent,afip,by.x="razon_social",by.y="nombre")

### Match/merge Autoridades con merge anterior

try2 <- merge(igj,try,by.x="ï..numero_correlativo",by.y="numero_correlativo")

### Exportar a TXT archivo de datos
write.table(try2,"mergeEntAutAfip.txt",sep=",",row.names=FALSE)
