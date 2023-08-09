import mysql.connector
from mysql.connector import Error
import pandas as pd
import streamlit as st 
import os


def make_xls(df,name):
    df.to_excel(f'{name}.xlsx', index=False)

    print(f'xls creado {name}') 

def make_xlsreturn(df,name):
    file=df.to_excel(f'{name}.xlsx', index=False)

    print(f'xls creado {name}') 
    return file 


# Set the database connection details
host = '3.138.116.85'
database = 'rivero-system-production'
user = 'elpidio'
password = 'elpidiop455w0rd'

# Declare the connection variable outside the try block
connection = None

table_names=[]

sstt = 1
if sstt == 1:
    year_check=st.selectbox(f'precontractYear ?  ',['2019','2020','2021','2022','2023'])
    name_result=st.text_input("name to response file 'fileName'    ")
else:    
    year_check=input(f'precontractYear ?  ')
    name_result=input("name to response file 'fileName'    ")

######
contract_status=[
        'ALL',
        'VACANT',
        'STARTED',
        'FINISHED',
        'CANCELLED',
        'READY BUT PENDING PAYABLE',
        'PROCESSING_PERMIT',
        'WAITING FOR THE CUSTOMER',
        'DOWNLOADING FILES',
        'SENT TO SALES OFFICE',
        'IN PRODUCTION QUEUE',
        'SENT TO ENGINEER',
        'WAITING FOR ADMINISTRATION',
        'EXPORTED TO NEW COMPANY']

status_contract_user=st.multiselect('Status',contract_status)
action=st.button('Search')

if name_result == '' and action == True:
    name_result=input("give me a name to response file 'namefile'    ")
else:
    action = False

def conexion_():
    connection = mysql.connector.connect(
        host=host,
        database=database,
        user=user,
        password=password
    )

    cursor=connection.cursor() 
    
    return cursor,connection


def contracts_status(cursor,conexion,list_status): 
    print(contracts_status)

    data_proyectcontract=[]
    data_projectNocontract=[]

    print('1')
    #cursor.execute("show columns from contract_status")
    #contStatusId	contStatusCode	language	contStatusName

    columns_contract_status=['contStatusCode','contStatusName']#[x[0] for x in cursor]
    print('2')
    #cursor.execute("select contStatusCode,contStatusName,language from contract_status")
    #cursor.execute("select * from contract_status")
    #data_status_contract=[x for x in cursor]
    
    contract_status_dict={
        '1':'VACANT',
        '2':'STARTED',
        '3':'FINISHED',
        '4':'CANCELLED',
        '5':'READY BUT PENDING PAYABLE',
        '6':'PROCESSING_PERMIT',
        '7':'WAITING FOR THE CUSTOMER',
        '8':'DOWNLOADING FILES',
        '9':'SENT TO SALES OFFICE',
        '10':'IN PRODUCTION QUEUE',
        '11':'SENT TO ENGINEER',
        '12':'WAITING FOR ADMINISTRATION',
        '13':'EXPORTED TO NEW COMPANY'
    }
     
    print('contract_status_dict',contract_status_dict)

    
    #df3=pd.DataFrame('Fecha a consultar',data_status_contract,columns=columns_contract_status)
    #make_xls(df3,'ContractStatus')
    
    
    
    
    print('sentence',"select * from pre_contract where contractid is not NULL")
    if year_check in [str(x) for x in range(2019,2024)]:

        cursor.execute(f"select * from pre_contract where contractid is not NULL and precontractDate like '{year_check}%'")
        data_proyectcontract=[x for x in cursor]

    else:
        cursor.execute(f"select * from pre_contract where contractid is not NULL")
        data_proyectcontract=[x for x in cursor]


    for x in data_proyectcontract:
        pass#print(x)

    

    #cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'pre_contract'") 
    #table_columns=[]
    #for x in cursor:
    #    table_columns.append(x[0])
    table_columns=[
        'precontractId',
        'preId',
        'contractType',
        'projectName',
        'countryId',
        'companyId',
        'precontractDate',
        'clientId', 	
        'propertyNumber',
        'streetName',
        'streetType',
        'suiteNumber',
        'city',
        'state',
        'zipCode',
        'buildingCodeId',
        'groupId',
        'projectUseId',
        'constructionType',
        'comment',	
        'precontractCost',
        'currencyId',
        'contractId',
        'userId',
        'deleted_at',
 	    'updated_at'
    ]
    
    ##print('table_columns',table_columns)
    df=pd.DataFrame(data_proyectcontract,columns=table_columns)
    df1=df[['precontractId',
        'preId',
        'contractType',
        'projectName',
        'countryId',
        'companyId',
        'precontractDate',
        'streetName',
        'streetType',
        'suiteNumber',
        'city',
        'state',
        'zipCode',
        'buildingCodeId',
        'contractId']]
    
    make_xls(df1,'ProjectsToContract')
    
    cursor.execute("show columns from contract")
    columns_contract=[x[0] for x in cursor]
    
    cursor.execute("select * from contract")
    data_contract=[]
    for x in cursor:
        #condition_status=contract_status_dict[x[31]]
        #list(x).extend(condition_status)
        data_contract.append(x)

    df2=pd.DataFrame(data_contract,columns=columns_contract)
    make_xls(df2,'Contracts')
    
    
    # ids de proyectos que pasaron a contratos 
    #df1['contractId'] ### proyectos a contrato en df1 



    ####### consultar contract para ver el estatus del proyecto 
    cursor.execute("select contractId,contractNumber,contractStatus,contractDate,clientId,propertyNumber,startDate,scheduledFinishDate,actualFinishDate,deliveryDate,initialComment,intermediateComment,finalComment from contract")

    data_contracts=[]
    for x in cursor:
        if x[0] in df1['contractId']:
            print('project to contract')
        #print('clave',x[2])
        #print('valor',contract_status_dict[str(x[2])])
            data_contracts.append([x[0],x[1],contract_status_dict[str(x[2])],x[3],x[4],x[5],x[6],x[7],x[8],x[9],x[10],x[11],x[12]])
        else: 
            print('no project') 

    df3=pd.DataFrame(data_contracts,columns=['contractId','contractNumber','contractStatus','contractDate','clientId','propertyNumber','startDate','scheduledFinishDate','actualFinishDate','deliveryDate','initialComment','intermediateComment','finalComment'])
    if name_result == '':
        make_xls(df3,f'Contracts_actual_status')
        
    else:
        
        
        # Ruta al archivo Excel dentro de la carpeta del proyecto 
        
        ###### filtrar el contract status 
        
        # Lista de valores a incluir
     

        # Filtrar usando .isin()
        df3_object = df3[df3['contractStatus'].isin(list_status)]
        
        make_xls(df3_object,f'./{name_result}')
        excel_file = f'./{name_result}.xlsx'

        st.dataframe(df3_object)

        if os.path.exists(excel_file):
            with open(excel_file, 'rb') as f:
                data = f.read()
            st.download_button(
                label='Descargar Reporte Excel',
                data=data,
                file_name=os.path.basename(excel_file),
                mime='application/vnd.ms-excel'
            )
                
        else:
            st.error('El archivo Excel no existe')

try:
    # Connect to the MySQL server
    connection = mysql.connector.connect(
        host=host,
        database=database,
        user=user,
        password=password
    )

    # Check if the connection is successful
    if connection.is_connected():
        db_info = connection.get_server_info()
        print("Connected to MySQL Server version", db_info)

        # Execute a sample query to test the connection
        cursor = connection.cursor()
        cursor.execute("SELECT DATABASE();")
        record = cursor.fetchone()
        print("You're connected to database:", record[0])

except Error as e:
    print("Error while connecting to MySQL:", e)

finally:
    # Close the cursor and connection
    if connection is not None and connection.is_connected():
        cursor.execute("SHOW TABLES;")
        results = cursor.fetchall()
        
        for row in results:

            if 'contract' in row[0]: 
                table_names.append(row[0])
            else:
                pass 

        #cursor.close()
        #connection.close()
        print("MySQL connection is closed")
        print('table_names',table_names)
        
        if len(status_contract_user) > 0 and action == False: 
            contracts_status(cursor,connection,status_contract_user)
        else:
            pass 

