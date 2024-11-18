### Services nécessaires pour la configuration et la sécurité sur Azure :

1. **Azure Container Registry (ACR)** – Stockage des images Docker.
2. **Azure Container Instances (ACI)** – Exécution des images Docker.
3. **Azure Blob Storage** – Stockage de 25 Go de données.
4. **Azure SQL Database - Serverless** – Base de données SQL.
5. **Azure Key Vault** – Sécurisation des secrets et clés d'API.
6. **Azure Active Directory (Azure AD)** – Gestion des utilisateurs et des accès.
7. **Network Security Group (NSG) + Virtual Network (VNet)** – Sécurisation du réseau.
8. **Azure Monitor & Azure Security Center** – Surveillance de la sécurité et gestion des vulnérabilités.
9. **TLS/SSL** – Sécurisation des communications entre les services.

---

### Résumé des coûts par mois :

- **Azure Container Registry (ACR)** : 5 $  
- **Azure Container Instances (ACI)** : 0,40 $  
- **Azure Blob Storage** : 0,46 $  
- **Azure SQL Database - Serverless** : 4,99 $  
- **Azure Key Vault** : ~1 $  
- **Azure Active Directory (Azure AD)** : gratuit (version de base)  
- **Network Security Group (NSG) + VNet** : coûts négligeables  
- **Azure Monitor & Azure Security Center** : gratuit pour un usage de base  
- **TLS/SSL** : gratuit (via HTTPS sur vos services)

### **Total estimé** : **12,85 $/mois**  
(dans une configuration de base avec des services de sécurité minimes).

