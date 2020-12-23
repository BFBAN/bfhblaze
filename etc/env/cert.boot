enableFiberStackCheck = true

#define BLAZE_SERVICE_NAME "BlazeSamples-2009-#PLATFORM#"

// XLSP and Redirector configuration, you will not need to modify these settings
#define XBOX_360_SERVICE_ID "0x45410004"
#define XBOX_360_LSP_NAME "scert-iad"
#define REDIRECTOR_ADDRESS "internal.gosredirector.scert.ea.com"
#define XBOX_360_SITE_NAME_SJC "scert-iad"
#define XBOX_360_SITE_NAME_IAD "scert-iad"
#define XBOX_360_SITE_NAME_GVA "scert-iad"

// QoS servers
#define QOS_SERVER_NAME_SJC "gossjcscert-qos01.beta.ea.com"
#define QOS_SERVER_NAME_IAD "gosiadscert-qos01.beta.ea.com"
#define QOS_SERVER_NAME_GVA "gosgvascert-qos01.beta.ea.com"

#define TELEM_SERVER "159.153.244.67"
#define TELEM_PORT 9986

// GPS Server
#define GPS_SERVER_NAME "becs.ea.com"
#define GPS_SERVER_PORT 80
#define GPS_CONNECTION_POOL_SIZE 4

#define DBHOST "scertgosmydb1.abn-iad.ea.com"
#define DBPORT 3306
#define DBBASE "gos_blaze_samples_#PLATFORM#"
#define DBUSER "blaze_user"
#define DBPASS "blaze_user"
#define DBMIN 1
#define DBMAX 8
#define DBCLIENT "MYSQL"

#define LFUHOST "gos.scert.ea.com"
#define LFUPORT 80
#if PLATFORM == "ps3"
    #define LFUEXTPORT 80
#elif PLATFORM == "xbl2"
    #define LFUEXTPORT 90
#endif

#define FUSIONHOST "novafusion.integration.ea.com:80"
#define FUSION_POOLSIZE 16
#define NUCLEUSHOST "nucleus.integration.ea.com"
#define NUCLEUS_POOLSIZE 128
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
    monitorMail = "GOSAlerts@ea.com"

    // E-mail addresses for the monitor to notify on server crash - not restarted
    monitorNotRestartedMail = "GOSCriticalAlerts@ea.com"

    // Monitor restart threshold
    monitorAllowedCrashCount = 3
    monitorAllowedCrashTime = 10

    // E-mail addresses for deploy notification
    deployMail = "GOSAlerts@ea.com"
}

#include "blaze.boot"



