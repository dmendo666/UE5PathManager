#pragma once
 
#include "Kismet/BlueprintFunctionLibrary.h"
#include "GameFramework/Actor.h"
#include "GetActorLabel.generated.h"
 
UCLASS()
class MYPROJECT2_API  UGetActorLabel : public UBlueprintFunctionLibrary
{
    GENERATED_BODY()
 
public:
    /** Retorna el label del actor (visible en World Outliner). En build empaquetado retorna el nombre interno. */
    UFUNCTION(BlueprintCallable, Category="Actor")
    static FString GetActorLabel(const AActor* Actor);
};