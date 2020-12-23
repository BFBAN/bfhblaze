enableFiberStackCheck = true

#define ENV "prod-m3d-dfw01"
#ifndef BLAZE_SERVICE_NAME
    #define BLAZE_SERVICE_NAME "qos-2010-#ENV#"
#endif


// XLSP and Redirector configuration, you will not need to modify these settings
#define XBOX_360_SERVICE_ID "0x45410004"
#define XBOX_360_LSP_NAME ""
#define REDIRECTOR_ADDRESS "internal.gosredirector.ea.com"
#define XBOX_360_SITE_NAME_SJC "prod-sjc"
#define XBOX_360_SITE_NAME_IAD "prod-iad"
#define XBOX_360_SITE_NAME_GVA "prod-gva"

// QoS servers
#define QOS_SERVER_NAME_SJC "gossjcstest-qos01.ea.com"
#define QOS_SERVER_NAME_IAD "gosiadstest-qos01.ea.com"
#define QOS_SERVER_NAME_GVA "gosgvastest-qos01.ea.com"

#define TELEM_SERVER "159.153.239.205"
#define TELEM_PORT 9986

// GPS server
#define GPS_SERVER_NAME "becs.integration.ea.com"
#define GPS_SERVER_PORT 80
#define GPS_CONNECTION_POOL_SIZE 4

#ifndef DBHOST
    #define DBHOST "gosprod-qos01.m3d-dfw.ea.com"
#endif
#ifndef DBPORT
    #define DBPORT 3306
#endif
#ifndef DBBASE
    #define DBBASE "qos"
#endif
#ifndef DBUSER
    #define DBUSER "qos_user"
    #define DBPASS "qos_user"
#endif
#define DBMIN 1
#define DBMAX 8
#define DBCLIENT "MYSQL"

#define LFUHOST "gos.ea.com"
#define LFUPORT 80
#define LFUEXTPORT 80

// NOTE: If NUCLEUSHOST changes then CRM_HOST, CSEMAILHOST and USIONHOST
// must also change as they are dependant.
#define NUCLEUSHOST "nucleus.integration.ea.com"
#define NUCLEUS_POOLSIZE 128
#define FUSIONHOST "novafusion.integration.ea.com:80"
#define FUSION_POOLSIZE 16
#define CRM_HOST "becs.integration.ea.com:80"
#define CRM_POOLSIZE 24
#define CSEMAILHOST "betacsrapp01.beta.eao.abn-iad.ea.com:8001"
#define TOSHOST "tos.ea.com:80"
#define TOS_POOLSIZE 128
#define OFBHOST "simsclubstore.ofb.integration.ea.com:80"
#define KEYMASTERHOST "keymaster.integration.ea.com:80"

// Source id in Nucleus  used to identify where a particular user registers or authenticate.
#define SOURCEID "134165"

// NOTE: If CUSTOMTOSHOST and CUSTOMTOSURI are not defined, Blaze will download default TOS.
// Or the client can define them as one of two cases below:
// ** 1. Client wants to override Blaze default TOS URL
//#define CUSTOMTOSHOST "sdevbesl01.online.ea.com:80"
//#define CUSTOMTOSURI "/easo/editorial/common/2010/tos/cstos.jsp?style=accept&lang=$LANG$&platform=xbl2"
// ** 2. Client doesn't want BlazeSDK to attempt to download TOS (Note: Only works with BlazeSDK 2.5 or above)
//#define CUSTOMTOSHOST
//#define CUSTOMTOSURI

deployInfo = {
    // E-mail addresses for the monitor to notify on server crash
    monitorMail = "GOSCriticalAlerts@ea.com"

    // E-mail addresses for the monitor to notify on server crash - not restarted
    monitorNotRestartedMail = "GOSCriticalAlerts@ea.com"

    // Monitor restart threshold
    monitorAllowedCrashCount = 3
    monitorAllowedCrashTime = 10

    // E-mail addresses for deploy notification    
    deployMail = "GOSAlerts@ea.com"
}

#include "blaze.boot"
