#pragma once

class Timer {
private:
    unsigned long interval = 0;
    bool running = false;
    bool finished = false;

public:
    unsigned long startTime = 0;
    void start(unsigned long ms) {
        interval = ms;
        startTime = millis();
        running = true;
        finished = false;
    }

    bool isFinished() {
        if (finished) return true;

        if (!running) return false;

        if (millis() - startTime >= interval) {
            running = false;
            finished = true;
            return true;
        }
        return false;
    }

    void reset() {
        startTime = millis();
        running = true;
        finished = false;
    }

    inline void stop() {
        running = false;
        finished = false;
    }

    inline float progress() const {
        if (finished) return 1.0f;
        if (!running) return 0.0f;

        unsigned long dt = millis() - startTime;
        return (dt >= interval) ? 1.0f : float(dt) / float(interval);
    }

    inline bool active() const {
        return running;
    }
};