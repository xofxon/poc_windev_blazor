using System;
using Microsoft.AspNetCore.Components;

namespace Generated
{
    public partial class pentnom : ComponentBase
    {

        public void Window_Declaration()
        {
            /* Original WLang:
               procedure pentnom (AppMode,codart,codnom,indnom,pNoSeq=0)
               GLOBAL
               	gModif est un booleen
               	gNomReq,glNomUpd est une chaine
               	of_entlien est un BDAPX_entlien
               	//
            */
            
            // Translated (heuristic):
            // TODO translate: procedure pentnom (AppMode,codart,codnom,indnom,pNoSeq=0)
            // TODO translate: GLOBAL
            	// TODO translate: gModif est un booleen
            	// TODO translate: gNomReq,glNomUpd est une chaine
            	// TODO translate: of_entlien est un BDAPX_entlien
            	//
        }

        public void On_Window_Event_34()
        {
            /* Original WLang:
               pf_init()
            */
            
            // Translated (heuristic):
            // TODO translate: pf_init()
        }

        public void On_blur_COD_ART()
        {
            /* Original WLang:
                        si cod_art <> "" alors
                           si pas ff_sellibelle ("cod_art")
                        	  ToastAffiche("Article inexistant.")
                        	  reprisesaisie(cod_art)
                           fin
                        fin
                       type : 16 (Sortie du champ)
            */
            
            // Translated (heuristic):
                     // TODO translate: si cod_art <> "" alors
                        // TODO translate: si pas ff_sellibelle ("cod_art")
                     	  // TODO translate: ToastAffiche("Article inexistant.")
                     	  // TODO translate: reprisesaisie(cod_art)
                        // TODO translate: fin
                     // TODO translate: fin
                    // TODO translate: type : 16 (Sortie du champ)
        }

        public void On_input_COD_ART()
        {
            /* Original WLang:
                        gModif=vrai
                       type : 17 (Chaque modification du champ)
            */
            
            // Translated (heuristic):
                     // TODO translate: gModif=true
                    // TODO translate: type : 17 (Chaque modification du champ)
        }

        public void On_click_BART()
        {
            /* Original WLang:
                        Resultat est une chaine
                        Resultat=""
                        ouvre(pselart,Resultat,"")
                        SI Resultat<>"" ALORS
                        	cod_art=Resultat
                        	ff_sellibelle ("cod_art")
                        	gModif=vrai
                        FIN
                       type : 18 (Clic sur bouton, image,etc)
            */
            
            // Translated (heuristic):
                     // TODO translate: Resultat est une chaine
                     // TODO translate: Resultat=""
                     // TODO translate: ouvre(pselart,Resultat,"")
                     // TODO translate: SI Resultat<>"" ALORS
                     	// TODO translate: cod_art=Resultat
                     	// TODO translate: ff_sellibelle ("cod_art")
                     	// TODO translate: gModif=true
                     // TODO translate: FIN
                    // TODO translate: type : 18 (Clic sur bouton, image,etc)
        }

        public void On_input_IND_NOM()
        {
            /* Original WLang:
                        gModif=Vrai
                       type : 17 (Chaque modification du champ)
            */
            
            // Translated (heuristic):
                     // TODO translate: gModif=true
                    // TODO translate: type : 17 (Chaque modification du champ)
        }

        public void On_input_ECOD_NOM()
        {
            /* Original WLang:
                        gModif=Vrai
                       type : 17 (Chaque modification du champ)
            */
            
            // Translated (heuristic):
                     // TODO translate: gModif=true
                    // TODO translate: type : 17 (Chaque modification du champ)
        }

        public void On_input_LIB_NOM()
        {
            /* Original WLang:
                        gModif=Vrai
                       type : 17 (Chaque modification du champ)
            */
            
            // Translated (heuristic):
                     // TODO translate: gModif=true
                    // TODO translate: type : 17 (Chaque modification du champ)
        }

        public void On_input_TYP_NOM()
        {
            /* Original WLang:
                        gModif = vrai
                        Si AppMode <> 0 alors reprisesaisie()
                        Selon TYP_NOM
                        Cas 1
                        	ECOD_NOM=4
                        CAS 2
                        	ECOD_NOM=5
                        CAS 3
                        	ECOD_NOM=1
                        CAS 4
                        	ECOD_NOM=3
                        AUTRES CAS
                        	ECOD_NOM=6
                        Fin
                       type : 17 (Chaque modification du champ)
            */
            
            // Translated (heuristic):
                     // TODO translate: gModif = true
                     // TODO translate: Si AppMode <> 0 alors reprisesaisie()
                     // TODO translate: Selon TYP_NOM
                     // TODO translate: Cas 1
                     	// TODO translate: ECOD_NOM=4
                     // TODO translate: CAS 2
                     	// TODO translate: ECOD_NOM=5
                     // TODO translate: CAS 3
                     	// TODO translate: ECOD_NOM=1
                     // TODO translate: CAS 4
                     	// TODO translate: ECOD_NOM=3
                     // TODO translate: AUTRES CAS
                     	// TODO translate: ECOD_NOM=6
                     // TODO translate: Fin
                    // TODO translate: type : 17 (Chaque modification du champ)
        }

        public void On_input_DAT_DEBUTI()
        {
            /* Original WLang:
                        gModif=Vrai
                       type : 17 (Chaque modification du champ)
            */
            
            // Translated (heuristic):
                     // TODO translate: gModif=true
                    // TODO translate: type : 17 (Chaque modification du champ)
        }

        public void On_input_DAT_FINUTI()
        {
            /* Original WLang:
                        gModif=Vrai
                       type : 17 (Chaque modification du champ)
            */
            
            // Translated (heuristic):
                     // TODO translate: gModif=true
                    // TODO translate: type : 17 (Chaque modification du champ)
        }

        public void On_click_BOK()
        {
            /* Original WLang:
                        Si gModif alors
                        	SauveObjet()
                        	si gModif alors // Si erreur de saisie
                        		reprisesaisie(COD_ART)
                        	fin
                        FIN
                        ferme
                       type : 18 (Clic sur bouton, image,etc)
            */
            
            // Translated (heuristic):
                     // TODO translate: Si gModif alors
                     	// TODO translate: SauveObjet()
                     	// TODO translate: si gModif alors // Si erreur de saisie
                     		// TODO translate: reprisesaisie(COD_ART)
                     	// TODO translate: fin
                     // TODO translate: FIN
                     // TODO translate: ferme
                    // TODO translate: type : 18 (Clic sur bouton, image,etc)
        }

        public void On_click_QUITTE()
        {
            /* Original WLang:
                        pf_TestSauve()
                        Ferme
                       type : 18 (Clic sur bouton, image,etc)
            */
            
            // Translated (heuristic):
                     // TODO translate: pf_TestSauve()
                     // TODO translate: Ferme
                    // TODO translate: type : 18 (Clic sur bouton, image,etc)
        }

        public void On_init_ModèleDeChamps1()
        {
            /* Original WLang:
                           igenerique : Declare_Fen()
                          type : 14 (Initialisation du champ)
            */
            
            // Translated (heuristic):
                        // TODO translate: igenerique : Declare_Fen()
                       // TODO translate: type : 14 (Initialisation du champ)
        }

        public void On_click_ModèleDeChamps1()
        {
            /* Original WLang:
                           OuvreMenuContextuel(MCTX_BTNAIDE)
                          type : 18 (Clic sur bouton, image,etc)
            */
            
            // Translated (heuristic):
                        // TODO translate: OuvreMenuContextuel(MCTX_BTNAIDE)
                       // TODO translate: type : 18 (Clic sur bouton, image,etc)
        }

        public void On_typeunk_ModèleDeChamps1()
        {
            /* Original WLang:
            */
            
            // No translation available
        }

        public void On_init_ModèleDeChamps1_1()
        {
            /* Original WLang:
                        //Exécute le traitement défini dans le modèle
                        ExécuteAncêtre
                       type : 14 (Initialisation du champ)
            */
            
            // Translated (heuristic):
                     //Exécute le traitement défini dans le modèle
                     // TODO translate: ExécuteAncêtre
                    // TODO translate: type : 14 (Initialisation du champ)
        }

        public void On_focus_ModèleDeChamps1()
        {
            /* Original WLang:
                        //Exécute le traitement défini dans le modèle
                        ExécuteAncêtre
                       type : 15 (Entrée dans le champ)
            */
            
            // Translated (heuristic):
                     //Exécute le traitement défini dans le modèle
                     // TODO translate: ExécuteAncêtre
                    // TODO translate: type : 15 (Entrée dans le champ)
        }

        public void On_blur_ModèleDeChamps1()
        {
            /* Original WLang:
                        //Exécute le traitement défini dans le modèle
                        ExécuteAncêtre
                       type : 16 (Sortie du champ)
            */
            
            // Translated (heuristic):
                     //Exécute le traitement défini dans le modèle
                     // TODO translate: ExécuteAncêtre
                    // TODO translate: type : 16 (Sortie du champ)
        }

        public void On_affectation_ModèleDeChamps1()
        {
            /* Original WLang:
                        //Exécute le traitement défini dans le modèle
                        ExécuteAncêtre
                       type : 43 (Affectation de la propriété valeur)
            */
            
            // Translated (heuristic):
                     //Exécute le traitement défini dans le modèle
                     // TODO translate: ExécuteAncêtre
                    // TODO translate: type : 43 (Affectation de la propriété valeur)
        }

        public void On_récupération_ModèleDeChamps1()
        {
            /* Original WLang:
                        //Exécute le traitement défini dans le modèle
                        ExécuteAncêtre
                       type : 42 (Récupération de la propriété valeur)
            */
            
            // Translated (heuristic):
                     //Exécute le traitement défini dans le modèle
                     // TODO translate: ExécuteAncêtre
                    // TODO translate: type : 42 (Récupération de la propriété valeur)
        }

        public void On_input_ModèleDeChamps1()
        {
            /* Original WLang:
                        //Exécute le traitement défini dans le modèle
                        ExécuteAncêtre
                       type : 17 (Chaque modification du champ)
            */
            
            // Translated (heuristic):
                     //Exécute le traitement défini dans le modèle
                     // TODO translate: ExécuteAncêtre
                    // TODO translate: type : 17 (Chaque modification du champ)
        }

        public void On_typeunk_ModèleDeChamps1_1()
        {
            /* Original WLang:
            */
            
            // No translation available
        }

        public void On_init_ModèleDeChamps1_2()
        {
            /* Original WLang:
                           type : 14 (Initialisation du champ)
            */
            
            // Translated (heuristic):
                        // TODO translate: type : 14 (Initialisation du champ)
        }

        // Procédure originale : pentnom
        /*
        si cod_art <> "" alors
           si pas ff_sellibelle ("cod_art")
        	  ToastAffiche("Article inexistant.")
        	  reprisesaisie(cod_art)
           fin
        fin
        */
        public void pentnom()
        {
            // TODO translate: si cod_art <> "" alors
               // TODO translate: si pas ff_sellibelle ("cod_art")
            	  // TODO translate: ToastAffiche("Article inexistant.")
            	  // TODO translate: reprisesaisie(cod_art)
               // TODO translate: fin
            // TODO translate: fin
        }

        // Procédure originale : BTN_MODELE_AIDE
        /*
        OuvreMenuContextuel(MCTX_BTNAIDE)
        */
        public void BTN_MODELE_AIDE()
        {
            // TODO translate: OuvreMenuContextuel(MCTX_BTNAIDE)
        }

        // Procédure originale : _Menu
        /*
        sChaineAideDefaut est une chaine
        QUAND EXCEPTION DANS
        	sChaineAideDefaut = {FenEnExécution()+".AideIssueDeReQuete",indVariable}
        FAIRE
        	sChaineAideDefaut =""
        FIN
        ouvre(Fen_Notes_Fen,FenEnExécution(),{FenEnExécution(),indFenêtre}..Titre,sChaineAideDefaut)
        */
        public void _Menu()
        {
            // TODO translate: sChaineAideDefaut est une chaine
            // TODO translate: QUAND EXCEPTION DANS
            	// TODO translate: sChaineAideDefaut = {FenEnExécution()+".AideIssueDeReQuete",indVariable}
            // TODO translate: FAIRE
            	// TODO translate: sChaineAideDefaut =""
            // TODO translate: FIN
            // TODO translate: ouvre(Fen_Notes_Fen,FenEnExécution(),{FenEnExécution(),indFenêtre}..Titre,sChaineAideDefaut)
        }

        // Procédure originale : MCTX_BTNAIDE
        /*
        sChaineAideDefaut est une chaine
        QUAND EXCEPTION DANS
        	sChaineAideDefaut = {FenEnExécution()+".AideIssueDeReQuete",indVariable}
        FAIRE
        	sChaineAideDefaut =""
        FIN
        ouvre(Fen_Notes_Fen,FenEnExécution(),{FenEnExécution(),indFenêtre}..Titre,sChaineAideDefaut)
        */
        public void MCTX_BTNAIDE()
        {
            // TODO translate: sChaineAideDefaut est une chaine
            // TODO translate: QUAND EXCEPTION DANS
            	// TODO translate: sChaineAideDefaut = {FenEnExécution()+".AideIssueDeReQuete",indVariable}
            // TODO translate: FAIRE
            	// TODO translate: sChaineAideDefaut =""
            // TODO translate: FIN
            // TODO translate: ouvre(Fen_Notes_Fen,FenEnExécution(),{FenEnExécution(),indFenêtre}..Titre,sChaineAideDefaut)
        }

        // Procédure originale : Notedaide
        /*
        sChaineAideDefaut est une chaine
        QUAND EXCEPTION DANS
        	sChaineAideDefaut = {FenEnExécution()+".AideIssueDeReQuete",indVariable}
        FAIRE
        	sChaineAideDefaut =""
        FIN
        ouvre(Fen_Notes_Fen,FenEnExécution(),{FenEnExécution(),indFenêtre}..Titre,sChaineAideDefaut)
        */
        public void Notedaide()
        {
            // TODO translate: sChaineAideDefaut est une chaine
            // TODO translate: QUAND EXCEPTION DANS
            	// TODO translate: sChaineAideDefaut = {FenEnExécution()+".AideIssueDeReQuete",indVariable}
            // TODO translate: FAIRE
            	// TODO translate: sChaineAideDefaut =""
            // TODO translate: FIN
            // TODO translate: ouvre(Fen_Notes_Fen,FenEnExécution(),{FenEnExécution(),indFenêtre}..Titre,sChaineAideDefaut)
        }

        // Procédure originale : MCTX_opt_Traduc
        /*
        SI FenEtat(FEN_Traduction_Element) = Inexistant ALORS
        	Ouvresoeur(FEN_Traduction_Element,FenEnCours())
        SINON
        	Info("La fenêtre de traduction est déjà ouverte.","Veuillez enregistrer vos modifications et fermer la fenêtre.")
        FIN
        */
        public void MCTX_opt_Traduc()
        {
            // TODO translate: SI FenEtat(FEN_Traduction_Element) = Inexistant ALORS
            	// TODO translate: Ouvresoeur(FEN_Traduction_Element,FenEnCours())
            // TODO translate: SINON
            	// TODO translate: Info("La fenêtre de traduction est déjà ouverte.","Veuillez enregistrer vos modifications && fermer la fenêtre.")
            // TODO translate: FIN
        }

        // Procédure originale : Case1
        /*
           procedure pentnom (AppMode,codart,codnom,indnom,pNoSeq=0)
           GLOBAL
           	gModif est un booleen
           	gNomReq,glNomUpd est une chaine
           	of_entlien est un BDAPX_entlien
           	//
        -
        */
        public void Case1()
        {
               // TODO translate: procedure pentnom (AppMode,codart,codnom,indnom,pNoSeq=0)
               // TODO translate: GLOBAL
               	// TODO translate: gModif est un booleen
               	// TODO translate: gNomReq,glNomUpd est une chaine
               	// TODO translate: of_entlien est un BDAPX_entlien
               	//
            // TODO translate: -
        }

        // Procédure originale : SauveObjet
        /*
        procedure SauveObjet()
        
        pf_verifobligatoire ()
        AVEC of_entlien
        	.LIB_NOM=LIB_NOM
        	.typ_nom=TYP_NOM
        	.dat_debutil=DAT_DEBUTI
        	.DAT_FINUTIl=DAT_FINUTI
        	.dat_modi=DAT_MODI
        	:f_update("id_lien_dt="+.id_lien_dt)
        FIN
        gModif=Faux
        AppMode=1
        */
        public void SauveObjet()
        {
            // TODO translate: procedure SauveObjet()
            // TODO translate: 
            // TODO translate: pf_verifobligatoire ()
            // TODO translate: AVEC of_entlien
            	// TODO translate: .LIB_NOM=LIB_NOM
            	// TODO translate: .typ_nom=TYP_NOM
            	// TODO translate: .dat_debutil=DAT_DEBUTI
            	// TODO translate: .DAT_FINUTIl=DAT_FINUTI
            	// TODO translate: .dat_modi=DAT_MODI
            	// TODO translate: :f_update("id_lien_dt="+.id_lien_dt)
            // TODO translate: FIN
            // TODO translate: gModif=false
            // TODO translate: AppMode=1
        }

        // Procédure originale : ff_sellibelle
        /*
        procedure ff_sellibelle (champ) : booléen
        si champ = "cod_art" alors
        	(LIB_ART,LIB_ART2)=OP_MEAPX:f_Libart(COD_ART)
        	si SansEspace(LIB_ART)="" alors
        	     cod_art=""
                 renvoyer faux
              sinon
        	     renvoyer vrai
        	 FIN
        fin
        */
        public void ff_sellibelle()
        {
            // TODO translate: procedure ff_sellibelle (champ) : booléen
            // TODO translate: si champ = "cod_art" alors
            	// TODO translate: (LIB_ART,LIB_ART2)=OP_MEAPX:f_Libart(COD_ART)
            	// TODO translate: si SansEspace(LIB_ART)="" alors
            	     // TODO translate: cod_art=""
                     // TODO translate: renvoyer false
                  // TODO translate: sinon
            	     // TODO translate: renvoyer true
            	 // TODO translate: FIN
            // TODO translate: fin
        }

        // Procédure originale : pf_TestSauve
        /*
        procedure pf_TestSauve()
        Si gModif alors
          Si ouinon("Vous avez fait des modifications."+RC+...
                  "Voulez-vous les enregistrer ?") alors
        	SauveObjet()
          fin
        FIN
        */
        public void pf_TestSauve()
        {
            // TODO translate: procedure pf_TestSauve()
            // TODO translate: Si gModif alors
              // TODO translate: Si ouinon("Vous avez fait des modifications."+RC+...
                      // TODO translate: "Voulez-vous les enregistrer ?") alors
            	// TODO translate: SauveObjet()
              // TODO translate: fin
            // TODO translate: FIN
        }

        // Procédure originale : pf_verifobligatoire
        /*
        procédure pf_verifobligatoire()
        si cod_art = "" alors
           ToastAffiche("Article obligatoire.")
           reprisesaisie(cod_art)
        fin
        si ECOD_NOM = "" ou ECOD_NOM = 0 alors
           ToastAffiche("Numéro de nomenclature obligatoire.")
           reprisesaisie(ECOD_NOM)
        fin
        si ind_nom = "" alors
           ToastAffiche("Indice de nomenclature obligatoire.")
           reprisesaisie(ind_nom)
        fin
        si lib_nom = "" alors
           ToastAffiche("Libellé de nomenclature obligatoire.")
           reprisesaisie(lib_nom)
        fin
        si typ_nom = "" alors
           ToastAffiche("Type obligatoire.")
           reprisesaisie(typ_nom)
        fin
        */
        public void pf_verifobligatoire()
        {
            // TODO translate: procédure pf_verifobligatoire()
            // TODO translate: si cod_art = "" alors
               // TODO translate: ToastAffiche("Article obligatoire.")
               // TODO translate: reprisesaisie(cod_art)
            // TODO translate: fin
            // TODO translate: si ECOD_NOM = "" || ECOD_NOM = 0 alors
               // TODO translate: ToastAffiche("Numéro de nomenclature obligatoire.")
               // TODO translate: reprisesaisie(ECOD_NOM)
            // TODO translate: fin
            // TODO translate: si ind_nom = "" alors
               // TODO translate: ToastAffiche("Indice de nomenclature obligatoire.")
               // TODO translate: reprisesaisie(ind_nom)
            // TODO translate: fin
            // TODO translate: si lib_nom = "" alors
               // TODO translate: ToastAffiche("Libellé de nomenclature obligatoire.")
               // TODO translate: reprisesaisie(lib_nom)
            // TODO translate: fin
            // TODO translate: si typ_nom = "" alors
               // TODO translate: ToastAffiche("Type obligatoire.")
               // TODO translate: reprisesaisie(typ_nom)
            // TODO translate: fin
        }

        // Procédure originale : pf_init
        /*
        PROCEDURE pf_init()
        gModif=Faux
        //	On ne vient qu'en mode modification
        COD_ART = codart
        COD_ART..Etat = Grisé
        BART..Etat = Grisé
        ECOD_NOM = codnom
        ECOD_NOM..Etat = Grisé
        IND_NOM = indnom
        IND_NOM..Etat = Grisé
        */
        public void pf_init()
        {
            // TODO translate: PROCEDURE pf_init()
            // TODO translate: gModif=false
            //	On ne vient qu'en mode modification
            // TODO translate: COD_ART = codart
            // TODO translate: COD_ART..Etat = Grisé
            // TODO translate: BART..Etat = Grisé
            // TODO translate: ECOD_NOM = codnom
            // TODO translate: ECOD_NOM..Etat = Grisé
            // TODO translate: IND_NOM = indnom
            // TODO translate: IND_NOM..Etat = Grisé
        }

    }
}