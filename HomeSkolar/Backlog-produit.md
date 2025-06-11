# Backlog Produit - HomeSkolar

# Backlog Produit - HomeSkolar

| ID | User Story (FR) | Utilisateur | Back-end | Front-end | Critères d’acceptation | Priorité | Estimation (jours) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| US1 | En tant qu’utilisateur, je veux créer un compte afin de pouvoir accéder à l’application. | Élève / Tuteur | API création utilisateur + validation + email confirmation | Formulaire inscription, validation client, messages d’erreur/succès | Formulaire complet, compte créé, mail de confirmation reçu | Must | 3 |
| US2 | En tant qu’utilisateur, je veux me connecter à l’aide de mes identifiants pour accéder à mon espace personnel. | Élève / Tuteur | API d’authentification + gestion session/token | Formulaire login, gestion erreurs, redirection | Connexion réussie, accès espace personnel | Must | 2 |
| US3 | En tant qu’utilisateur, je veux réinitialiser mon mot de passe en cas d’oubli. | Élève / Tuteur | API envoi lien réinitialisation, changement mdp | Formulaire demande réinitialisation + changement | Lien envoyé, mot de passe modifié | Must | 3 |
| US4 | En tant qu’utilisateur, je veux envoyer un message à mon interlocuteur pour rester en contact. | Élève / Tuteur | API CRUD messages, stockage en base | Interface messagerie texte, rafraîchissement temps réel | Messages envoyés et reçus instantanément | Must | 4 |
| US5 | En tant qu’utilisateur, je veux être notifié lorsqu’un nouveau message m’est adressé. | Élève / Tuteur | API notifications, récupération messages non lus | Badge et popup notification en temps réel | Notification visible dès qu’un message arrive | Must | 2 |
| US6 | En tant qu’utilisateur, je veux pouvoir épingler un message important pour le retrouver facilement. | Élève / Tuteur | API marquage/démarquage message épinglé | Bouton épingler/favori, vue dédiée épinglés | Messages épinglés affichés dans liste dédiée | Should | 3 |
| US7 | En tant qu’utilisateur, je veux planifier un rendez-vous avec mon interlocuteur. | Élève / Tuteur | API création, modification, suppression rendez-vous | Formulaire calendrier interactif | Rendez-vous créés et visibles dans calendrier | Must | 5 |
| US8 | En tant qu’utilisateur, je veux visualiser tous mes rendez-vous passés et futurs. | Élève / Tuteur | API récupération rendez-vous avec filtres | Vue calendrier/liste avec filtres | Tous les rendez-vous affichés correctement | Must | 3 |
| US9 | En tant qu’élève, je veux voir mes tâches à réaliser après une rencontre avec mon tuteur. | Élève | API création tâche liée rendez-vous | Liste tâches + formulaire ajout | Tâches liées au rendez-vous visibles et consultables | Must | 4 |
| US10 | En tant qu’élève, je veux marquer une tâche comme terminée pour suivre ma progression. | Élève | API mise à jour statut tâche | Checkbox/bouton terminer, affichage visuel | Statut tâche modifié et affiché visuellement | Must | 2 |
| US11 | En tant qu’utilisateur, je veux créer une tâche personnelle (note ou mémo). | Élève / Tuteur | API création tâche indépendante | Formulaire tâche perso (titre + description) | Tâche personnelle visible dans la liste des tâches | Should | 3 |
| US12 | En tant qu’utilisateur, je veux recevoir une notification avant un rendez-vous. | Élève / Tuteur | Scheduler notifications programmées | Popup/badge notification dans app | Notification reçue 24h ou 1h avant rendez-vous | Should | 3 |
| US13 | En tant qu’élève, je veux recevoir un rappel pour une tâche proche de son échéance. | Élève | Scheduler notification tâches à échéance | Notification visuelle et/ou email | Rappel reçu à J-1 ou jour même | Could | 2 |

---

# Synthèse

- **Must Have** : 31 jours
- **Should Have** : 9 jours
- **Could Have** : 2 jours
- **Total estimé** : 42 jours (hors tests, UI design, intégration)

---