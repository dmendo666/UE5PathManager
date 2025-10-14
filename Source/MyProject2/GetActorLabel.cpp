// GetActorLabel.cpp
#include "GetActorLabel.h"

FString UGetActorLabel::GetActorLabel(const AActor* Actor)
{
    if (!Actor)
    {
        return FString();
    }

#if WITH_EDITOR
    return Actor->GetActorLabel();
#else
    return Actor->GetName();
#endif
}