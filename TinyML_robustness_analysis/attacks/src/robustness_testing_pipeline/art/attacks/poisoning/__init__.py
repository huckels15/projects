"""
Module providing poisoning attacks under a common interface.
"""
from art.attacks.poisoning.backdoor_attack_dgm.backdoor_attack_dgm_red import BackdoorAttackDGMReDTensorFlowV2
from art.attacks.poisoning.backdoor_attack_dgm.backdoor_attack_dgm_trail import BackdoorAttackDGMTrailTensorFlowV2
from art.attacks.poisoning.backdoor_attack import PoisoningAttackBackdoor
from art.attacks.poisoning.poisoning_attack_svm import PoisoningAttackSVM
from art.attacks.poisoning.feature_collision_attack import FeatureCollisionAttack
from art.attacks.poisoning.adversarial_embedding_attack import PoisoningAttackAdversarialEmbedding
from art.attacks.poisoning.clean_label_backdoor_attack import PoisoningAttackCleanLabelBackdoor
from art.attacks.poisoning.bullseye_polytope_attack import BullseyePolytopeAttackPyTorch
from art.attacks.poisoning.gradient_matching_attack import GradientMatchingAttack
from art.attacks.poisoning.hidden_trigger_backdoor.hidden_trigger_backdoor import HiddenTriggerBackdoor
from art.attacks.poisoning.hidden_trigger_backdoor.hidden_trigger_backdoor_pytorch import HiddenTriggerBackdoorPyTorch
from art.attacks.poisoning.hidden_trigger_backdoor.hidden_trigger_backdoor_keras import HiddenTriggerBackdoorKeras