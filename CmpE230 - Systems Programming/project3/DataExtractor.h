#ifndef DATAEXTRACTOR_H
#define DATAEXTRACTOR_H
#include <QtNetwork/QNetworkAccessManager>
#include <QMainWindow>
#include <vector>

namespace Ui {
class DataExtractor;
}

class DataExtractor : public QMainWindow
{
    Q_OBJECT

public:
    explicit DataExtractor(QWidget *parent = 0);
    ~DataExtractor();

public slots:
    void CoinsList(QNetworkReply * reply) ;         // save the result of the first query, which represents every accepted coin in the api
    void replyFinished(QNetworkReply * reply) ;     // save the result of the second query, which contains exchange-rate data
    QString getData();                              // return the result, which contains exchange-rate data
    std::vector<std::string> getCryptos();          // get the list of crypto-currencies extracted from the input file

private:
    QNetworkAccessManager *manager1;    // manages first query
    QNetworkAccessManager *manager2;    // manages second query
    QString result;                     // exchange-rate data
    QString coins;                      // data of every accepted coin in the api
    std::vector<std::string> cryptos;   // list of crypto-currencies extracted from the input file
};

#endif // DATAEXTRACTOR_H
