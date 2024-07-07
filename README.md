# le-her

[english readme](README-EN.md)

## Vorraussetzungen

Benötigte Programme :
- Python 3 (https://www.python.org/)

Benötigte Python Module :
- numpy (https://numpy.org/)
    >> pip install numpy
- pyqt5 (https://pypi.org/project/PyQt5/)
    >> pip install PyQt5
    
## Spielregeln

Le Her is ein 2-Spieler Spiel (hier wird ein Spieler durch die Spiel KI ersetzt).  
Ein Spieler übernimmt die Rolle der Dealers und der andere die Rolle des Spielers.  
Eine Runde Le Her beginnt damit das zuerst der Spieler und dann der Dealer eine Karte vom Deck ziehen.  
Dann hat der Spieler die Option seine akutelle Karte mit der akutellen Karte der Dealers zu tauschen.  
Falls der Dealer einen König hat, wird nicht getauscht.  
In beiden fällen werden die Karten dem anderen Spieler gezeigt.  
Danach hat der Dealer die Option eine neue Karte vom deck zu ziehen und seine aktuelle Karte oben auf das Deck zurück zu legen.  
Falls die neu gezogene Karte ein König ist, behällt der Dealer sein Karte und der König wird wieder oben auf das Deck gelegt.  
In beiden fällen wird dem Spieler weder die neue Karte noch die akutelle Karte des Dealers gezeigt.  
Danach ist die Runde vorbei und es geht wieder von vorne los.  
Ein Le Her Spiel besteht aus 13 Runden.  
Danach zählt jeder Spieler die Punkte seiner 13 Karten zusammen (Ass = 1p, 2 = 2p, ..., 10 = 10p, Bube = 11p, Dame = 12p, König = 13p).  
Der Spiler mit der höheren Gesamtpunktzahl hat gewonnen.  
