#include "DataExtractor.h"
#include <QtNetwork/QNetworkAccessManager>
#include <QtNetwork/QNetworkReply>
#include <QRegularExpression>
#include <QEventLoop>
#include <QUrl>
#include <vector>
#include <string>
#include <iostream>
#include <fstream>

std::string getEnvironmentVariable( std::string const& env)
{
    char *val = getenv( env.c_str() );
    return val == NULL ? std::string("") : std::string(val);
}

DataExtractor::DataExtractor(QWidget *parent) :
    QMainWindow(parent)
{
    this->manager1 = new QNetworkAccessManager(this);

    // Connect QNetWorkAccessManager with this DataExtractor
    // CoinsList() will be called when the QNetworkAccessManager receives reply
    connect(manager1,
            &QNetworkAccessManager::finished,
            this,
            &DataExtractor::CoinsList);

    // Make a query to access coins accepted by the website
    QString URL = QString("https://api.coingecko.com/api/v3/coins/list");
    QUrl url1(URL);
    QNetworkReply* reply1 = manager1->get(QNetworkRequest(url1));

    // By connecting finished() signal of the reply to quit() slot, we are able to wait
    // for the reply to finish before proceeding with the rest of the procedure.
    QEventLoop loop1;
    connect(reply1, SIGNAL(finished()), &loop1, SLOT(quit()));
    loop1.exec();

    // get the absolute path of the file and open it
    std::string path = getEnvironmentVariable("MYCRYPTOCONVERT");
    std::ifstream infile;
    infile.open(path);

    for( std::string line; getline( infile, line ); )
    {
        // If there is a '.' in the line, then we need to replace it with "\." before using regex.
        QString coin = QString::fromStdString(line);
        coin.replace(QRegularExpression("\\."), QString("\\."));

        // Try matching the line assuming that it is a crypto ID
        QRegularExpression cryptoPattern1(QString("{\"id\":\"")+coin+QString("\",\"symbol\":\"([^\"]+)\",\"name\":\"([^\"]+)\"}"));
        QRegularExpressionMatch cryptoMatch = cryptoPattern1.match(this->coins);
        if(cryptoMatch.hasMatch()) {  // ID
            // Check if the ID exists in the list of possible crypto IDs
            if(!std::count(this->cryptos.begin(), this->cryptos.end(), line))
                this->cryptos.push_back(line);
            continue;
        }

        // Try matching the line assuming that it is a crypto SYMBOL
        QRegularExpression cryptoPattern2(QString("{\"id\":\"([^\"]+)\",\"symbol\":\"")+coin+QString("\",\"name\":\"([^\"]+)\"}"));
        cryptoMatch = cryptoPattern2.match(this->coins);
        if(cryptoMatch.hasMatch()) { // SYMBOL
            std::string found = cryptoMatch.captured(1).toLocal8Bit().constData();
            // Check if the ID (std::string found) exists in the list of possible crypto IDs.
            if(!std::count(this->cryptos.begin(), this->cryptos.end(), found))
                this->cryptos.push_back(found);
            continue;
        }

        // Try matching the line assuming that it is a crypto NAME
        QRegularExpression cryptoPattern3(QString("{\"id\":\"([^\"]+)\",\"symbol\":\"([^\"]+)\",\"name\":\"")+coin+QString("\""));
        cryptoMatch = cryptoPattern3.match(this->coins);
        if(cryptoMatch.hasMatch()) { // NAME
            std::string found = cryptoMatch.captured(1).toLocal8Bit().constData();
            // Check if the ID (std::string found) exists in the list of possible crypto IDs.
            if(!std::count(this->cryptos.begin(), this->cryptos.end(), found))
                this->cryptos.push_back(found);
            continue;
        }
        infile.close();
    }

    // Connect QNetWorkAccessManager with this DataExtractor
    // replyFinished() will be called when the QNetworkAccessManager receives reply
    this->manager2 = new QNetworkAccessManager(this);
    connect(manager2,
            &QNetworkAccessManager::finished,
            this,
            &DataExtractor::replyFinished);

    // construct url using extracted crypto currencies and make the request
    std::string currency;
    for (const std::string &c : this->cryptos) currency += c +",";
    currency = currency.substr(0, currency.size()-1);
    QString URL2 = QString::fromStdString("https://api.coingecko.com/api/v3/simple/price?ids="+currency+"&vs_currencies=usd,eur,gbp");
    QUrl url2(URL2);
    QNetworkReply* reply2 = manager2->get(QNetworkRequest(url2));

    // By connecting finished() signal of the reply to quit() slot, we are able to wait
    // for the reply to finish before proceeding with the rest of the procedure.
    QEventLoop loop2;
    connect(reply2, SIGNAL(finished()), &loop2, SLOT(quit()));
    loop2.exec();
}

// save the result of the first query, which represents every accepted coin in the api
void DataExtractor::CoinsList(QNetworkReply *reply) {
    this->coins = (QString) reply->readAll();
}

// save the result of the second query, which contains exchange-rate data
void DataExtractor::replyFinished(QNetworkReply *reply) {
    this->result = (QString) reply->readAll();
}

// return the result, which contains exchange-rate data
QString DataExtractor::getData() {
    return this->result;
}

// get the list of crypto-currencies extracted from the input file
std::vector<std::string> DataExtractor::getCryptos()
{
    return this->cryptos;
}

DataExtractor::~DataExtractor()
{
    delete this->manager1;
    delete this->manager2;
}
