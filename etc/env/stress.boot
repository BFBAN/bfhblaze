enableFiberStackCheck = true

#define BLAZE_SERVICE_NAME "gosblaze-#DEV_USER_NAME#-#PLATFORM#-stress"
// XLSP and Redirector configuration, you will not need to modify these settings
#define XBOX_360_SERVICE_ID "0x45410004"
#define XBOX_360_LSP_NAME ""
#define REDIRECTOR_ADDRESS "internal.gosredirector.stest.ea.com"

#define XBOX_360_SITE_NAME_SJC "stest-sjc"
#define XBOX_360_SITE_NAME_IAD "stest-iad"
#define XBOX_360_SITE_NAME_GVA "stest-gva"

// QoS servers
#define QOS_SERVER_NAME_SJC "gossjcstest-qos01.beta.ea.com"
#define QOS_SERVER_NAME_IAD "gosiadstest-qos01.beta.ea.com"
#define QOS_SERVER_NAME_GVA "gosgvastest-qos01.beta.ea.com"

#define TELEM_SERVER "159.153.239.205"
#define TELEM_PORT 9986

// GPS server
#define GPS_SERVER_NAME "becs.integration.ea.com"
#define GPS_SERVER_PORT 80
#define GPS_CONNECTION_POOL_SIZE 4

#define DBHOST "sltgosmydb1b.abn-iad.ea.com"
#define DBPORT 3306

// developer please create and use your own schema/login
// ** DO NOT use demo database blaze_user **
// please use the form unixusername if you have not yet created one
// Or you can customize DBBASE, DBUSER, DBPASS individually below
#define DBBASE "#DEV_USER_NAME#"
#define DBUSER "#DEV_USER_NAME#"
#define DBPASS "#DEV_USER_NAME#"
#define DBMIN 128
#define DBMAX 128
#define DBCLIENT "MYSQL"

//user to access registration db (supposed to have only select privilege)
#define DBREGUSER "registration_user"
#define DBREGPASS "registration_password"

#define LFUHOST "gos.stest.ea.com"
#define LFUPORT 8000
#if PLATFORM == "ps3"
    #define LFUEXTPORT 80
#elif PLATFORM == "xbl2"
    #define LFUEXTPORT 90
#endif

// NOTE: If NUCLEUSHOST changes then CRM_HOST, CSEMAILHOST and USIONHOST
// must also change as they are dependant.
#define NUCLEUSHOST "nucleus.staging.ea.com"
#define NUCLEUS_POOLSIZE 128
#define FUSIONHOST "novafusion.integration.ea.com:80"
#define FUSION_POOLSIZE 16
//for prod, it should be "#define CRM_HOST "becs.ea.com:80""
#define CRM_HOST "becs.integration.ea.com:80"
#define CRM_POOLSIZE 16
#define CSEMAILHOST "betacsrapp01.beta.eao.abn-iad.ea.com:8001"
#define TOSHOST "betos.ea.com:80"
#define TOS_POOLSIZE 128
#define OFBHOST "simsclubstore.ofb.integration.ea.com:80"
#define KEYMASTERHOST "keymaster.integration.ea.com:80"

// Allow fake stress accounts to login for the stress environment
#define ALLOW_STRESS_LOGIN "true"

// Source id in Nucleus  used to identify where a particular user registers or authenticate.
#define SOURCEID "134165"

//Group Name for Online Play entitlement
#define ONLINE_PLAY_GROUPNAME "SPORE"

// NOTE: If CUSTOMTOSHOST and CUSTOMTOSURI are not defined, Blaze will download default TOS.
// Or the client can define them as one of two cases below:
// ** 1. Client wants to override Blaze default TOS URL
//#define CUSTOMTOSHOST "sdevbesl01.online.ea.com:80"
//#define CUSTOMTOSURI "/easo/editorial/common/2010/tos/cstos.jsp?style=accept&lang=$LANG$&platform=xbl2"
// ** 2. Client doesn't want BlazeSDK to attempt to download TOS (Note: Only works with BlazeSDK 2.5 or above)
// #define CUSTOMTOSHOST
// #define CUSTOMTOSURI


deployInfo = {
    // E-mail addresses for the monitor to notify on server crash
    monitorMail = "nobody@ea.com"

    // E-mail addresses for the monitor to notify on server crash - not restarted
    monitorNotRestartedMail = "nobody@ea.com"

    // Monitor restart threshold
    monitorAllowedCrashCount = 3
    monitorAllowedCrashTime = 10

    // E-mail addresses for deploy notification
    deployMail = "nobody@ea.com"
}

#include "blaze.boot"