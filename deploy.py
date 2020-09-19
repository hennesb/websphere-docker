'''
Sample deployment file for Websphere on docker
'''


ORACLE_DRIVER_VARIABLE_NAME = "ORACLE_JDBC_DRIVER_PATH"
newVarValue = "/opt/IBM/WebSphere/AppServer/lib"


global AdminConfig

def logEnvironment():
    print('Logging environment details')
    print('Running on Java version: ' + java.lang.System.getProperty('java.version'))
    print('Java Home : ' + java.lang.System.getProperty('java.home'))
    print('Operating System Name : ' + java.lang.System.getProperty('os.name'))



def connectionPoolProperties():
    return ['connectionPool', [ ['agedTimeout', 100], ["maxConnections","12"], ["minConnections","0"] ] ]


def dsJNDIName():
    return ['jndiName', 'jdbc/appds']

def authAlias():
    return ['authDataAlias', 'appDataBaseAlias']


def sqlStatmentCache():
    return ['statementCacheSize', 200]

def mappingAlias():
    return ["mapping",[["authDataAlias","appDataBaseAlias"], ["mappingConfigAlias","DefaultPrincipalMapping"]]]

def customeProperties():
    return ['propertySet', [['resourceProperties', [[['name', 'URL'], ['type', 'String'], ['value', 'jdbc:oracle:thin:@docker.for.mac.host.internal:1521:xe']]]]]]



def dataSoureAttributes():
    return  [ dsJNDIName(), connectionPoolProperties(), authAlias(), sqlStatmentCache(), mappingAlias(), customeProperties() ]


def createDataSource():
    print('Creating JDBC provider for Oracle')
    jdbc_provider=AdminJDBC.createJDBCProvider("DefaultNode01", "server1", "Oracle JDBC provider", "oracle.jdbc.pool.OracleConnectionPoolDataSource",[['classpath', '${ORACLE_JDBC_DRIVER_PATH}/ojdbc8.jar'], ['providerType', 'Oracle JDBC Driver']])
    print('**********')
    AdminConfig.listTemplates('JDBCProvider')
    print('Creating datasource ..')
    dataSource=AdminJDBC.createDataSource("DefaultNode01", "server1", "Oracle JDBC provider", "Oracle DataSource", dataSoureAttributes() )
    return jdbc_provider
    


def createJ2CAuthDetailsForOracle():
    print('Creating J2C auth alias')
    security = AdminConfig.getid('/Cell:DefaultCell01/Security:/')
    alias = ['alias', 'appDataBaseAlias']
    userid = ['userId', 'db_user']
    password = ['password', 'secret']
    jaasAttrs = [alias, userid, password]
    AdminConfig.create('JAASAuthData', security, jaasAttrs)


def saveWebSphereConfig():
   print('Saving Websphere Configuration')
   AdminConfig.save()


def setWebsphereEnvVariable():
    node = AdminConfig.getid("/Node:DefaultNode01/")
    varSubstitutions = AdminConfig.list("VariableSubstitutionEntry",node).split(java.lang.System.getProperty("line.separator"))  
    for varSubst in varSubstitutions:
       getVarName = AdminConfig.showAttribute(varSubst, "symbolicName")
       if getVarName == ORACLE_DRIVER_VARIABLE_NAME:
          AdminConfig.modify(varSubst,[["value", newVarValue]])
          break



def installApplication():
    print('Installing application ...')
    print AdminApp.taskInfo('/work/InetAddressInfoTest.ear', 'MapWebModToVH')
    AdminApp.install('/work/InetAddressInfoTest.ear', '[-MapWebModToVH [[ "Inet Address Info Test" InetAddressInfoTest.war,WEB-INF/web.xml default_host ]] -appname dnsCacheTest]') 
    print('Application installed ')


def deploy():
    logEnvironment()
    setWebsphereEnvVariable()
    createJ2CAuthDetailsForOracle()
    createDataSource()
    installApplication()
    saveWebSphereConfig()


#
# Execute the deployment

deploy()

