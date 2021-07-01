#include <stdio.h>

#include "DataExtractor.h"

#include <QApplication>

#include <QGridLayout>
#include <QLabel>

#include <QStringList>
#include <QString>

#include <QRegularExpression>

#include <vector>
#include <string>
#include <iostream>
#include <unordered_map>

using namespace std;
int main(int argc, char *argv[])
{
    qputenv("QT_STYLE_OVERRIDE", 0);  // to avoid any environment variable issue
    QApplication a(argc, argv);

    QWidget       window ;      // main widget
    QGridLayout   gridLayout;   // layout with which the table is drawn
    DataExtractor extractor;

    // add the currencies we want to use
    vector<string> currencies;
    currencies.push_back("USD");
    currencies.push_back("EUR");
    currencies.push_back("GBP");

    // get names of the crypto-currencies extractor read from the file in MYCRYPTOCURRENCIES.
    vector<string> cryptos = extractor.getCryptos();


    // -------------
    // GET DATA
    // -------------

    QString result = extractor.getData();

    // --------------
    // PARSING
    // --------------

    unordered_map<string, vector<QString>> map; // to store (crpyto, exchange-rates) pairs

    QRegularExpression cryptoPattern("\"([\\w-]+)\":{([^}]*)}");                  // matches: "litecoin":{"usd":160.04,"eur":131.44,"gbp":113.04}
    QRegularExpression currencyPattern("\"([\\w-]+)\":(\\d+\\.?(e-?)?\\d*),?");   // matches: "usd":160.04,

    QRegularExpressionMatch cryptoMatch = cryptoPattern.match(result);
    while (cryptoMatch.hasMatch())
    {
        string cryptoLabel = cryptoMatch.captured(1).toLocal8Bit().constData(); // get crypto label
        QString currencySegment = cryptoMatch.captured(2);                      // get the segment containing exchange-rates of the crypto

        vector<QString> cryptoValues;   // to store exchange rates

        QRegularExpressionMatch currencyMatch = currencyPattern.match(currencySegment); // match exchange-rate
        while (currencyMatch.hasMatch())
        {
            cryptoValues.push_back(currencyMatch.captured(2));  // get the rate

            currencySegment = currencySegment.mid(currencyMatch.capturedEnd(0), currencySegment.length());  // remove the matched exhange-rate from the segment string
            currencyMatch = currencyPattern.match(currencySegment);                                         // try matchinging another exchange-rate, loop ends if there is no match
        }

        while(cryptoValues.size() < 3) cryptoValues.push_back("");              // if exchange-rate data is not found, we place empty string
        map.insert(pair<string, vector<QString>>(cryptoLabel, cryptoValues));   // add the (crpyto, exchange-rates) pair to the map

        result = result.mid(cryptoMatch.capturedEnd(0)+1, result.length());     // remove the matched crypto from the result string
        cryptoMatch = cryptoPattern.match(result);                              // try matchinging another crypto, loop ends if there is no match
    }

    // get the values from the map and store them in a vector
    vector<vector<QString>> values;
    for (string& crypto:cryptos) values.push_back(map[crypto]);

    // --------------
    // CREATING GRID
    // --------------

    // place holder QLabel. Placed to the upper-left corner.
    QLabel* numberLabel = new QLabel();
    numberLabel->setFrameStyle(QFrame::Box | QFrame::Plain);
    gridLayout.addWidget(numberLabel, 0, 0);

    for (unsigned long long x=0; x<currencies.size(); x++)
    {
        // see the documentation below for styling:
        // https://doc.qt.io/archives/qt-4.8/qframe.html#details
        QLabel* currencyLabel = new QLabel(QString::fromStdString(currencies[x]));  // create QLabel for currency
        currencyLabel->setFrameStyle(QFrame::Box | QFrame::Plain);                  // set QLabel style
        currencyLabel->setAlignment(Qt::AlignHCenter | Qt::AlignVCenter);           // set QLabel allignment
        gridLayout.addWidget(currencyLabel, 0, (int)x+1);                           // add currency QLabel to the grid
        for (unsigned long long y=0; y<cryptos.size(); y++)
        {
            QLabel* numberLabel = new QLabel(values[y][x]);                 // create QLabel for exchange-rate
            numberLabel->setFrameStyle(QFrame::Box | QFrame::Plain);        // set QLabel style
            numberLabel->setAlignment(Qt::AlignHCenter | Qt::AlignVCenter); // set QLabel allignment
            gridLayout.addWidget(numberLabel, (int)y+1, (int)x+1);          // add currency QLabel to the grid
        }
    }

    for (unsigned long long y=0; y<cryptos.size(); y++)
    {
        string crypto = cryptos[y];
        crypto[0] = toupper(crypto[0]) ;                                  // capitalize crypto ID
        QLabel* cryptoLabel = new QLabel(QString::fromStdString(crypto)); // create QLabel for crypto-currency.
        cryptoLabel ->setFrameStyle(QFrame::Box | QFrame::Plain);         // set QLabel style
        gridLayout.addWidget(cryptoLabel, (int)y+1, 0);                   // add crypto QLabel to the grid
    }

    // Adjust minimum size of the grid
    gridLayout.setColumnMinimumWidth(0, 180); // crypto labels
    for(int col=1; col < gridLayout.columnCount(); col++)
    {
        gridLayout.setColumnMinimumWidth(col, 120);
    }
    for(int row=0; row < gridLayout.rowCount(); row++)
    {
        gridLayout.setRowMinimumHeight(row, 40);
    }

    // Remove empty spaces between QLabel elements in the grid
    gridLayout.setHorizontalSpacing(0);
    gridLayout.setVerticalSpacing(0);

    window.setLayout(&gridLayout); // Set layout

    window.show();
    return a.exec();
}
