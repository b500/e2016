
# coding: utf-8

# In[ ]:


import os
e2016_home =  "/home/neilor/e2016"
e2016_tse_home = e2016_home+"/tse"
ufs=['PA','ES','RS','AM','MT','MG','PR','CE','BA','AL','SP','PI','GO','MS','AC','SE','PE','RJ','RR','AP','SC','RO','PB','TO','RN','MA','DF','BR']
os.chdir(e2016_tse_home)
connect_cmd = "dbname='e2016' user='neilor' host='localhost' password='n1f2c3n1'"
from sqlalchemy import create_engine
engine = create_engine('postgresql://neilor:n1f2c3n1@localhost:5432/e2016')
## conda install -c conda-forge ipython-sql 
get_ipython().magic('load_ext sql')
get_ipython().magic('sql postgresql://neilor:n1f2c3n1@/e2016')


# Tutorial de Postgres
# https://wiki.postgresql.org/wiki/Psycopg2_Tutorial

# In[ ]:


import psycopg2

try:
    conn = psycopg2.connect("dbname='e2016' user='neilor' host='localhost' password='n1f2c3n1'")
except:
    print ("I am unable to connect to the database")


# ## Cria schema para cada estado, DF e BR

# In[ ]:


for uf in ufs:
    create_schema = "CREATE SCHEMA tse_%s;" % uf.lower()
    get_ipython().magic('sql {create_schema}')


# ## Importa arquivos consulta_cand_2016 

# In[ ]:


import wget
url = 'http://agencia.tse.jus.br/estatistica/sead/odsele/consulta_cand/consulta_cand_2016.zip'
filename = wget.download(url)


# In[ ]:


import zipfile
zip_ref = zipfile.ZipFile(e2016_tse_home+"/consulta_cand_2016.zip", 'r')
zip_ref.extractall(e2016_tse_home+"/consulta_cand_2016")
zip_ref.close()


# In[ ]:


get_ipython().magic('rm {e2016_tse_home+"/consulta_cand_2016.zip"}')


# ## define tabela consulta_cand

# In[ ]:


def create_table_consulta_cand(table_name):
    query = """
        CREATE TABLE %s
        (
        data_geracao varchar,
        hora_geracao varchar,
        ano_eleicao varchar,
        num_turno varchar,
        descricao_eleicao varchar,
        sigla_uf varchar,
        sigla_ue varchar,
        descricao_ue varchar,
        codigo_cargo varchar,
        descricao_cargo varchar,
        nome_candidato varchar,
        sequencial_candidato varchar,
        numero_candidato varchar,
        cpf_candidato varchar,
        nome_urna_candidato varchar,
        cod_situacao_candidatura varchar,
        des_situacao_candidatura varchar,
        numero_partido varchar,
        sigla_partido varchar,
        nome_partido varchar,
        codigo_legenda varchar,
        sigla_legenda varchar,
        composicao_legenda varchar,
        nome_legenda varchar,
        codigo_ocupacao varchar,
        descricao_ocupacao varchar,
        data_nascimento varchar,
        num_titulo_eleitoral_candidato varchar,
        idade_data_eleicao varchar,
        codigo_sexo varchar,
        descricao_sexo varchar,
        cod_grau_instrucao varchar,
        descricao_grau_instrucao varchar,
        codigo_estado_civil varchar,
        descricao_estado_civil varchar,
        codigo_cor_raca varchar,
        descricao_cor_raca varchar,
        codigo_nacionalidade varchar,
        descricao_nacionalidade varchar,
        sigla_uf_nascimento varchar,
        codigo_municipio_nascimento varchar,
        nome_municipio_nascimento varchar,
        despesa_max_campanha varchar,
        cod_sit_tot_turno varchar,
        desc_sit_tot_turno varchar,
        nm_email varchar
        );""" % table_name

    cur = conn.cursor()
    cur.execute(query)
    conn.commit()
    cur.close()



# ## carrega tabelas consulta_cand 2016

# In[ ]:


def load_csv_into_table(table_name,file_csv):
    "upload de arquivo .csv em tabela "
    copy = """COPY %s FROM '%s' ( 
        FORMAT CSV,
        OIDS false,
        FREEZE false,
        DELIMITER ';',
        NULL '',
        HEADER false,
        QUOTE '"',
        ENCODING 'LATIN-1'
        ); """ % (table_name, file_csv)
    
    get_ipython().magic('sql {copy}')


# In[ ]:


import codecs
consulta_cand_dir = e2016_tse_home+"/consulta_cand_2016"

for root, dirs, files, rootfd in os.fwalk(consulta_cand_dir, topdown=False):
    for filename in files:
        file_full_name = consulta_cand_dir+'/'+filename
        name = filename.split(".")
        if name[1] == "txt":
            fname=name[0]
            uf = fname[-2:]
            table_name = ('tse_'+uf+'.'+fname).lower()
            print(table_name,' <-- ',file_full_name)
            create_table_consulta_cand(table_name)
            load_csv_into_table(table_name,file_full_name)


# ## Importa arquivos prestacao_contas_final_2016 

# In[ ]:


import wget
url='http://agencia.tse.jus.br/estatistica/sead/odsele/prestacao_contas/prestacao_contas_2016.zip'
#url = 'http://agencia.tse.jus.br/estatistica/sead/odsele/prestacao_contas/prestacao_contas_final_2016.zip'
filename = wget.download(url)


# In[ ]:


import zipfile
zip_ref = zipfile.ZipFile(e2016_tse_home+"/prestacao_contas_final_2016.zip", 'r')
zip_ref.extractall(e2016_tse_home+"/prestacao_contas_final_2016")
zip_ref.close()


# In[ ]:


get_ipython().magic('rm {e2016_tse_home+"/prestacao_contas_final_2016.zip"}')


# ## define tabelas despesas e receitas de candidatos e partidos

# In[ ]:


def create_despesas_partidos_2016(table_name):
    query = """
        DROP TABLE IF EXISTS  %s;
        CREATE TABLE %s
        (
        cod_eleicao varchar,
        desc_eleicao varchar,
        data_e_hora varchar,
        cnpj_prestador_conta varchar,
        sequencial_do_prestador_de_conta varchar,
        uf varchar,
        sigla_da_ue varchar,
        nome_da_ue varchar,
        tipo_diretorio varchar,
        sigla__partido varchar,
        tipo_do_documento varchar,
        numero_do_documento varchar,
        cpf_cnpj_do_fornecedor varchar,
        nome_do_fornecedor varchar,
        nome_do_fornecedor_receita_federal varchar,
        cod_setor_economico_do_fornecedor varchar,
        setor_economico_do_fornecedor varchar,
        data_da_despesa varchar,
        valor_despesa varchar,
        tipo_despesa varchar,
        descricao_da_despesa varchar
        )""" % (table_name,table_name)

    get_ipython().magic('sql {query}')


# In[ ]:


def create_despesas_candidatos_2016(table_name):
    query = """
        DROP TABLE IF EXISTS %s;
        CREATE TABLE %s
        (
        cod_eleicao varchar,
        desc_eleicao varchar,
        data_e_hora varchar,
        cnpj_prestador_conta varchar,
        sequencial_candidato varchar,
        uf varchar,
        sigla_da_ue varchar,
        nome_da_ue varchar,
        sigla__partido varchar,
        numero_candidato varchar,
        cargo varchar,
        nome_candidato varchar,
        cpf_do_candidato varchar,
        cpf_do_vice_suplente varchar,
        tipo_de_documento varchar,
        numero_do_documento varchar,
        cpf_cnpj_do_fornecedor varchar,
        nome_do_fornecedor varchar,
        nome_do_fornecedor_receita_federal varchar,
        cod_setor_economico_do_fornecedor varchar,
        setor_economico_do_fornecedor varchar,
        data_da_despesa varchar,
        valor_despesa varchar,
        tipo_despesa varchar,
        descricao_da_despesa varchar
        )""" % (table_name,table_name)

    get_ipython().magic('sql {query}')



# In[ ]:


def create_receitas_partidos_2016(table):
    query = """
        DROP TABLE IF EXISTS %s;
        CREATE TABLE %s
        (
        cod_eleicao varchar,
        desc_eleicao varchar,
        data_e_hora varchar,
        cnpj_prestador_conta varchar,
        sequencial_prestador_conta varchar,
        uf varchar,
        sigla_da_ue varchar,
        nome_da_ue varchar,
        tipo_diretorio varchar,
        sigla__partido varchar,
        numero_recibo_eleitoral varchar,
        numero_do_documento varchar,
        cpf_cnpj_do_doador varchar,
        nome_do_doador varchar,
        nome_do_doador_receita_federal varchar,
        sigla_ue_doador varchar,
        numero_partido_doador varchar,
        numero_candidato_doador varchar,
        cod_setor_economico_do_doador varchar,
        setor_economico_do_doador varchar,
        data_da_receita varchar,
        valor_receita varchar,
        tipo_receita varchar,
        fonte_recurso varchar,
        especie_recurso varchar,
        descricao_da_receita varchar,
        cpf_cnpj_do_doador_originario varchar,
        nome_do_doador_originario varchar,
        tipo_doador_originario varchar,
        setor_economico_do_doador_originario varchar,
        nome_do_doador_originario_receita_federal varchar
        );""" % (table_name,table_name)

    get_ipython().magic('sql {query}')


# In[ ]:


def create_receitas_candidatos_2016(table_name):
    query = """
        DROP TABLE IF EXISTS %s;
        CREATE TABLE %s
        (
        cod_eleicao varchar,
        desc_eleicao varchar,
        data_e_hora varchar,
        cnpj_prestador_conta varchar,
        sequencial_candidato varchar,
        uf varchar,
        sigla_da_ue varchar,
        nome_da_ue varchar,
        sigla__partido varchar,
        numero_candidato varchar,
        cargo varchar,
        nome_candidato varchar,
        cpf_do_candidato varchar,
        cpf_do_vice_suplente varchar,
        numero_recibo_eleitoral varchar,
        numero_do_documento varchar,
        cpf_cnpj_do_doador varchar,
        nome_do_doador varchar,
        nome_do_doador_receita_federal varchar,
        sigla_ue_doador varchar,
        numero_partido_doador varchar,
        numero_candidato_doador varchar,
        cod_setor_economico_do_doador varchar,
        setor_economico_do_doador varchar,
        data_da_receita varchar,
        valor_receita varchar,
        tipo_receita varchar,
        fonte_recurso varchar,
        especie_recurso varchar,
        descricao_da_receita varchar,
        cpf_cnpj_do_doador_originario varchar,
        nome_do_doador_originario varchar,
        tipo_doador_originario varchar,
        setor_economico_do_doador_originario varchar,
        nome_do_doador_originario_receita_federal varchar
        );""" % (table_name,table_name)

    get_ipython().magic('sql {query}')


# In[ ]:


def load_csv_into_table_h(table_name,file_csv):
    "upload de arquivo .csv em tabela "
    copy = """COPY %s FROM '%s' ( 
        FORMAT CSV,
        OIDS false,
        FREEZE false,
        DELIMITER ';',
        NULL '#NULO',
        HEADER TRUE,

        ENCODING 'LATIN-1'
        ); """ % (table_name, file_csv)
    
    get_ipython().magic('sql {copy}')


# ## carrega tabelas de receita e despesa

# In[ ]:


def load_tabelas(uf):
    prestacao_contas_dir = '/home/neilor/e2016/tse/prestacao_contas_final_2016/'
    tabela_schema = "tse_"+uf.lower()+'.'


    arq_desp_candidatos = prestacao_contas_dir+'despesas_candidatos_prestacao_contas_final_2016_'+uf.upper()+'.txt'
    tabela_desp_candidatos = tabela_schema+'despesas_candidatos_prestacao_contas_final_2016_'+uf.lower()
    print('despesas-candidatos\n',tabela_desp_candidatos,' <-- ',arq_desp_candidatos)
    create_despesas_candidatos_2016(tabela_desp_candidatos)
    load_csv_into_table_h(tabela_desp_candidatos,arq_desp_candidatos) 


    arq_rec_candidatos = prestacao_contas_dir+'receitas_candidatos_prestacao_contas_final_2016_'+uf.upper()+'.txt'
    tabela_rec_candidatos = tabela_schema+'receitas_candidatos_prestacao_contas_final_2016_'+uf.lower()
    print('receitas-candidatos\n',tabela_rec_candidatos,' <-- ',arq_rec_candidatos)
    create_receitas_candidatos_2016(tabela_rec_candidatos)
    load_csv_into_table_h(tabela_rec_candidatos,arq_rec_candidatos) 


    arq_desp_partidos = prestacao_contas_dir+'despesas_partidos_prestacao_contas_final_2016_'+uf.upper()+'.txt'
    tabela_desp_partidos = tabela_schema+'despesas_partidos_prestacao_contas_final_2016_'+uf.lower()
    print('despesas-partidos\n',tabela_desp_partidos,' <-- ',arq_desp_partidos)
    create_despesas_partidos_2016(tabela_desp_partidos)
    load_csv_into_table_h(tabela_desp_partidos,arq_desp_partidos)
 

    arq_rec_partidos = prestacao_contas_dir+'receitas_partidos_prestacao_contas_final_2016_'+uf.upper()+'.txt'
    tabela_rec_partidos = tabela_schema+'receitas_partidos_prestacao_contas_final_2016_'+uf.lower()
    print('receitas-partidos\n',tabela_rec_partidos,' <-- ',arq_rec_partidos)
    create_receitas_partidos_2016(tabela_rec_partidos)
    load_csv_into_table_h(tabela_rec_partidos,arq_rec_partidos)

load_tabelas('PR')


# ## copia de aruivo com problema de EOF ????

# In[ ]:


import codecs

file_i ='/home/neilor/e2016/tse/prestacao_contas_final_2016/despesas_candidatos_prestacao_contas_final_2016_SP.txt'
file_o ='/home/neilor/e2016/tse/prestacao_contas_final_2016/despesas_candidatos_prestacao_contas_final_2016_SP.txt_novo'

x = 0
l=''
fo=codecs.open(file_o,'w',encoding='latin1')
with codecs.open(file,'r',encoding='latin1') as f:
    for line in f: 
        l=line.replace('\0','')
        fo.write(l)
        x=x+1 
    fo.close()
    print(x)
    print(l)
    print()


