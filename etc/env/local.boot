enableFiberStackCheck = true

#define LOCAL_ONLY 1

#ifndef BASE_PORT
    #define BASE_PORT 43720
#endif

// PLATFORM needs to be a real platform (ps3, xbl2 are currently supported)
#ifndef PLATFORM
    #define PLATFORM "ps3"
#endif

#if PLATFORM == "xbl2"
    #define BASE_PORT BASE_PORT + 20
#endif

//gos developer's blaze servers
#define BLAZE_SERVICE_NAME "gosblaze-#DEV_USER_NAME#-#PLATFORM#"

// XLSP and Redirector configuration, you will not need to modify these settings
#define XBOX_360_SERVICE_ID "0x45410000"
#define XBOX_360_LSP_NAME ""
#define REDIRECTOR_ADDRESS "internal.gosredirector.online.ea.com"
#define XBOX_360_SITE_NAME_SJC "sdev-sjc"
#define XBOX_360_SITE_NAME_IAD "sdev-sjc"
#define XBOX_360_SITE_NAME_GVA "sdev-sjc"

// QoS servers
#define QOS_SERVER_NAME_SJC "python.online.ea.com"
#define QOS_SERVER_NAME_IAD "python.online.ea.com"
#define QOS_SERVER_NAME_GVA "python.online.ea.com"

#define TELEM_SERVER "10.30.80.234"
#define TELEM_PORT 9986

#define GPS_SERVER_NAME "becs.integration.ea.com"
#define GPS_SERVER_PORT 80
#define GPS_CONNECTION_POOL_SIZE 4

#ifndef DBHOST
    #define DBHOST "sdevgosmydb1.online.ea.com"
#endif
#ifndef DBPORT
    #define DBPORT 3306
#endif

// developer please create and use your own schema/login
// ** DO NOT use demo database blaze_user **
// please use the form unixusername if you have not yet created one
// Or you can customize DBBASE, DBUSER, DBPASS individually below

#ifndef DBBASE
    #define DBBASE "#DEV_USER_NAME#"
#endif
#ifndef DBUSER 
    #define DBUSER "#DEV_USER_NAME#"
#endif
#ifndef DBPASS 
    #define DBPASS "#DEV_USER_NAME#"
#endif
#define DBMAX 8
#define DBMIN 1
#define DBCLIENT "MYSQL"

//user to access registration db (supposed to have only select privilege)
#define DBREGUSER "registration_user"
#define DBREGPASS "registration_password"

#define LFUHOST "sdevbesl01.online.ea.com"
#define LFUPORT 8000
#define LFUEXTPORT 80

// NOTE: If NUCLEUSHOST changes then CRM_HOST, CSEMAILHOST and USIONHOST
// must also change as they are dependant.
#define NUCLEUSHOST "nucleus.integration.ea.com"
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