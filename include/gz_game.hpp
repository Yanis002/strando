#pragma once

#include <Game/Game.hpp>

// IMPORTANT: this should match `Game` exactly!
class CustomGame : public Game {
  public:
    void Run();
    void ExecutePause();
};
