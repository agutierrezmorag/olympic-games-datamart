/*==============================================================*/
/* DBMS name:      PostgreSQL 9.x                               */
/* Created on:     12-05-2024 15:44:40                          */
/*==============================================================*/


drop index ANIO_PK;

drop table ANIO;

drop index ATLETA_PK;

drop table ATLETA;

drop index CONTINENTE_PK;

drop table CONTINENTE;

drop index DEPORTE_PK;

drop table DEPORTE;

drop index DIM_GEOGRAFIA2_FK;

drop index ENTIDAD_PK;

drop table ENTIDAD;

drop index EVENTO_DEPORTIVO_PK;

drop table EVENTO_DEPORTIVO;

drop index DIM_ENTIDAD2_FK;

drop index DIM_TIEMPO2_FK;

drop index METRICAS_ENTIDADES_PK;

drop table METRICAS_ENTIDADES;

drop index DIM_DEPORTE2_FK;

drop index MODALIDAD_PK;

drop table MODALIDAD;

drop index DIM_DEPORTE_FK;

drop index DIM_ATLETA_FK;

drop index DIM_GEOGRAFIA_FK;

drop index DIM_EVENTO_DEPORTIVO_FK;

drop index DIM_TIEMPO_FK;

drop index RENDIMIENTO_ATLETICO_PK;

drop table RENDIMIENTO_ATLETICO;

/*==============================================================*/
/* Table: ANIO                                                  */
/*==============================================================*/
create table ANIO (
   IDANIO               INT4                 not null,
   constraint PK_ANIO primary key (IDANIO)
);

/*==============================================================*/
/* Index: ANIO_PK                                               */
/*==============================================================*/
create unique index ANIO_PK on ANIO (
IDANIO
);

/*==============================================================*/
/* Table: ATLETA                                                */
/*==============================================================*/
create table ATLETA (
   IDATLETA             INT4                 not null,
   NOMBREATLETA         VARCHAR(120)         not null,
   SEXOATLETA           VARCHAR(10)          not null,
   ANIONACIMIENTO       INT4                 not null,
   constraint PK_ATLETA primary key (IDATLETA)
);

/*==============================================================*/
/* Index: ATLETA_PK                                             */
/*==============================================================*/
create unique index ATLETA_PK on ATLETA (
IDATLETA
);

/*==============================================================*/
/* Table: CONTINENTE                                            */
/*==============================================================*/
create table CONTINENTE (
   IDCONTINENTE         INT4                 not null,
   CONTINENTE           VARCHAR(120)         not null,
   constraint PK_CONTINENTE primary key (IDCONTINENTE)
);

/*==============================================================*/
/* Index: CONTINENTE_PK                                         */
/*==============================================================*/
create unique index CONTINENTE_PK on CONTINENTE (
IDCONTINENTE
);

/*==============================================================*/
/* Table: DEPORTE                                               */
/*==============================================================*/
create table DEPORTE (
   IDDEPORTE            INT4                 not null,
   NOMBREDEPORTE        VARCHAR(120)         not null,
   constraint PK_DEPORTE primary key (IDDEPORTE)
);

/*==============================================================*/
/* Index: DEPORTE_PK                                            */
/*==============================================================*/
create unique index DEPORTE_PK on DEPORTE (
IDDEPORTE
);

/*==============================================================*/
/* Table: ENTIDAD                                               */
/*==============================================================*/
create table ENTIDAD (
   IDENTIDAD            INT4                 not null,
   IDCONTINENTE         INT4                 not null,
   ENTIDAD              VARCHAR(60)          not null,
   ALPHA3ENTIDAD        VARCHAR(3)           not null,
   NOCENTIDAD           VARCHAR(3)           not null,
   constraint PK_ENTIDAD primary key (IDENTIDAD)
);

/*==============================================================*/
/* Index: ENTIDAD_PK                                            */
/*==============================================================*/
create unique index ENTIDAD_PK on ENTIDAD (
IDENTIDAD
);

/*==============================================================*/
/* Index: DIM_GEOGRAFIA2_FK                                     */
/*==============================================================*/
create  index DIM_GEOGRAFIA2_FK on ENTIDAD (
IDCONTINENTE
);

/*==============================================================*/
/* Table: EVENTO_DEPORTIVO                                      */
/*==============================================================*/
create table EVENTO_DEPORTIVO (
   IDEVENTODEPORTIVO    INT4                 not null,
   NOMBREEVENTO         VARCHAR(120)         not null,
   TEMPORADAEVENTO      VARCHAR(120)         not null,
   CIUDADEVENTO         VARCHAR(120)         not null,
   PAISEVENTO           VARCHAR(120)         not null,
   CODIGOPAISEVENTO     VARCHAR(120)         not null,
   constraint PK_EVENTO_DEPORTIVO primary key (IDEVENTODEPORTIVO)
);

/*==============================================================*/
/* Index: EVENTO_DEPORTIVO_PK                                   */
/*==============================================================*/
create unique index EVENTO_DEPORTIVO_PK on EVENTO_DEPORTIVO (
IDEVENTODEPORTIVO
);

/*==============================================================*/
/* Table: METRICAS_ENTIDADES                                    */
/*==============================================================*/
create table METRICAS_ENTIDADES (
   IDHECHOENTIDAD       INT4                 not null,
   IDANIO               INT4                 not null,
   IDENTIDAD            INT4                 not null,
   IDH                  DECIMAL(8,2)         not null,
   ESCOLARIDAD          DECIMAL(8,2)         not null,
   GNI                  DECIMAL(8,2)         not null,
   POBLACION            INT4                 not null,
   constraint PK_METRICAS_ENTIDADES primary key (IDHECHOENTIDAD)
);

/*==============================================================*/
/* Index: METRICAS_ENTIDADES_PK                                 */
/*==============================================================*/
create unique index METRICAS_ENTIDADES_PK on METRICAS_ENTIDADES (
IDHECHOENTIDAD
);

/*==============================================================*/
/* Index: DIM_TIEMPO2_FK                                        */
/*==============================================================*/
create  index DIM_TIEMPO2_FK on METRICAS_ENTIDADES (
IDANIO
);

/*==============================================================*/
/* Index: DIM_ENTIDAD2_FK                                       */
/*==============================================================*/
create  index DIM_ENTIDAD2_FK on METRICAS_ENTIDADES (
IDENTIDAD
);

/*==============================================================*/
/* Table: MODALIDAD                                             */
/*==============================================================*/
create table MODALIDAD (
   IDMODALIDAD          INT4                 not null,
   IDDEPORTE            INT4                 not null,
   NOMBREMODALIDAD      VARCHAR(120)         not null,
   CATEGORIA            VARCHAR(120)         not null,
   constraint PK_MODALIDAD primary key (IDMODALIDAD)
);

/*==============================================================*/
/* Index: MODALIDAD_PK                                          */
/*==============================================================*/
create unique index MODALIDAD_PK on MODALIDAD (
IDMODALIDAD
);

/*==============================================================*/
/* Index: DIM_DEPORTE2_FK                                       */
/*==============================================================*/
create  index DIM_DEPORTE2_FK on MODALIDAD (
IDDEPORTE
);

/*==============================================================*/
/* Table: RENDIMIENTO_ATLETICO                                  */
/*==============================================================*/
create table RENDIMIENTO_ATLETICO (
   IDHECHORENDIMIENTO   INT4                 not null,
   IDANIO               INT4                 not null,
   IDEVENTODEPORTIVO    INT4                 not null,
   IDENTIDAD            INT4                 not null,
   IDATLETA             INT4                 not null,
   IDMODALIDAD          INT4                 not null,
   ESTATURA             DECIMAL              not null,
   PESO                 INT4                 not null,
   IMC                  DECIMAL              not null,
   EDAD                 INT4                 not null,
   TIPOPODIO            VARCHAR(20)          not null,
   EQUIPO               VARCHAR(120)         not null,
   RANGOETARIO          VARCHAR(120)         not null,
   constraint PK_RENDIMIENTO_ATLETICO primary key (IDHECHORENDIMIENTO)
);

/*==============================================================*/
/* Index: RENDIMIENTO_ATLETICO_PK                               */
/*==============================================================*/
create unique index RENDIMIENTO_ATLETICO_PK on RENDIMIENTO_ATLETICO (
IDHECHORENDIMIENTO
);

/*==============================================================*/
/* Index: DIM_TIEMPO_FK                                         */
/*==============================================================*/
create  index DIM_TIEMPO_FK on RENDIMIENTO_ATLETICO (
IDANIO
);

/*==============================================================*/
/* Index: DIM_EVENTO_DEPORTIVO_FK                               */
/*==============================================================*/
create  index DIM_EVENTO_DEPORTIVO_FK on RENDIMIENTO_ATLETICO (
IDEVENTODEPORTIVO
);

/*==============================================================*/
/* Index: DIM_GEOGRAFIA_FK                                      */
/*==============================================================*/
create  index DIM_GEOGRAFIA_FK on RENDIMIENTO_ATLETICO (
IDENTIDAD
);

/*==============================================================*/
/* Index: DIM_ATLETA_FK                                         */
/*==============================================================*/
create  index DIM_ATLETA_FK on RENDIMIENTO_ATLETICO (
IDATLETA
);

/*==============================================================*/
/* Index: DIM_DEPORTE_FK                                        */
/*==============================================================*/
create  index DIM_DEPORTE_FK on RENDIMIENTO_ATLETICO (
IDMODALIDAD
);

alter table ENTIDAD
   add constraint FK_ENTIDAD_DIM_GEOGR_CONTINEN foreign key (IDCONTINENTE)
      references CONTINENTE (IDCONTINENTE)
      on delete restrict on update restrict;

alter table METRICAS_ENTIDADES
   add constraint FK_METRICAS_DIM_ENTID_ENTIDAD foreign key (IDENTIDAD)
      references ENTIDAD (IDENTIDAD)
      on delete restrict on update restrict;

alter table METRICAS_ENTIDADES
   add constraint FK_METRICAS_DIM_TIEMP_ANIO foreign key (IDANIO)
      references ANIO (IDANIO)
      on delete restrict on update restrict;

alter table MODALIDAD
   add constraint FK_MODALIDA_DIM_DEPOR_DEPORTE foreign key (IDDEPORTE)
      references DEPORTE (IDDEPORTE)
      on delete restrict on update restrict;

alter table RENDIMIENTO_ATLETICO
   add constraint FK_RENDIMIE_DIM_ATLET_ATLETA foreign key (IDATLETA)
      references ATLETA (IDATLETA)
      on delete restrict on update restrict;

alter table RENDIMIENTO_ATLETICO
   add constraint FK_RENDIMIE_DIM_DEPOR_MODALIDA foreign key (IDMODALIDAD)
      references MODALIDAD (IDMODALIDAD)
      on delete restrict on update restrict;

alter table RENDIMIENTO_ATLETICO
   add constraint FK_RENDIMIE_DIM_EVENT_EVENTO_D foreign key (IDEVENTODEPORTIVO)
      references EVENTO_DEPORTIVO (IDEVENTODEPORTIVO)
      on delete restrict on update restrict;

alter table RENDIMIENTO_ATLETICO
   add constraint FK_RENDIMIE_DIM_GEOGR_ENTIDAD foreign key (IDENTIDAD)
      references ENTIDAD (IDENTIDAD)
      on delete restrict on update restrict;

alter table RENDIMIENTO_ATLETICO
   add constraint FK_RENDIMIE_DIM_TIEMP_ANIO foreign key (IDANIO)
      references ANIO (IDANIO)
      on delete restrict on update restrict;

