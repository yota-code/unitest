# à l'ouverture de session

se logguer sur sma6255

	ssh sma6255

lancer le shell zsh

	zsh

se déplacer dans le répertoire d'unitest

	cd /C/autools/source/$(whoami)/unitest

charger l'environnement

	source export_path

# à chaque nouvelle version du noeud

supprimer les includes à la con dans le fichier unitest/kcg/<node>/scade_type.h

installer la nouvelle instance 

	unitest_prepare <nom-du-neoud>

enfin, lancer le sénario pour le noeud choisi

	unitest_replay <node> <replay>


