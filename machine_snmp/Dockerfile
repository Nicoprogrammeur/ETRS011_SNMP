# Utiliser une image de base
FROM debian:buster-slim

# Installer le service SNMP
RUN apt-get update && apt-get install -y snmpd

# Copier la configuration SNMP
COPY snmpd.conf /etc/snmp/snmpd.conf

# Copier le script de simulation de traffic
COPY simulate_traffic.sh /usr/local/bin/simulate_in_traffic.sh
COPY simulate_traffic.sh /usr/local/bin/simulate_out_traffic.sh

# Rendre les scripts exécutables
RUN chmod +x /usr/local/bin/simulate_in_traffic.sh
RUN chmod +x /usr/local/bin/simulate_out_traffic.sh

# Exposer le port SNMP
EXPOSE 161/udp

# Commande à exécuter à chaque démarrage du conteneur
CMD ["snmpd", "-f", "-Lo"]