import timm
import torch

from pprint import pprint

if False:
    # query models
    models = timm.list_models("*efficientnet*", pretrained=True)

    print("Num models:", len(models))
    pprint(models)
else:
    # Pour implementation de Audio Spectrogram Transformer (AST):
    #    - fine tune deit veut dire aller chercher les poids directement dans le modele
    #      et les manipuler pour faire notre AST custom: relativement complique car il 
    #      faut connaitre deit meme si timm donne certains acces. D'autres modeles demandent
    #      de connaitre leur architecture aussi.
    # models = ["deit3_small_patch16_224.fb_in1k",
    #           "deit3_small_patch16_384.fb_in1k",
    #           "deit_small_patch16_224.fb_in1k",
    #           "deit_small_distilled_patch16_224.fb_in1k"]
    
    # Tests avec MobileVit de Apple - semble accepter n'importe quel size en input
    # mais donne tout simplement des embeddings avec size constant
    # Note: MobileVit semble le plus petit modele ayant de bonnes performances
    models = ["mobilevit_s.cvnets_in1k",
              "mobilevitv2_150.cvnets_in22k_ft_in1k"]
    
    # # Tests avec EfficientNet - repose sur CNN; semble un choix plus simple
    # # pour entrainement. Semble accepter n'importe quel size en input
    # # mais donne tout simplement des embeddings avec size constant
    # models = ["tf_efficientnetv2_s.in1k",
    #           "tf_efficientnetv2_m.in1k"]
    
    for m in models:
        print(m)

        model = timm.create_model(m, pretrained=True, num_classes=0, in_chans=1)

        # print("    num_patches:", model.patch_embed.num_patches)
        # print("    orig hw:", int(model.patch_embed.num_patches ** 0.5))
        # print("    embedding dim:", model.pos_embed.shape[2])
        # print("    cls_token:", model.cls_token.shape)
        # if hasattr(model, "dist_token"):
        #     print("    dist_token:", model.dist_token.shape)

        # config = timm.data.resolve_model_data_config(model)
        # pprint(config)

        x = torch.randn(1, 1, 128, 1024)
        output = model(x)
        print("   ", x.shape, "->", output.shape)

        print()
