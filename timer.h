class Timer {
private:
    unsigned long startTime = 0;
    unsigned long interval = 0;
    bool running = false;

public:
    void start(unsigned long ms) {
        interval = ms;
        startTime = millis();
        running = true;
    }

    bool isFinished() {
        if (!running) return false;

        if (millis() - startTime >= interval) {
            running = false;
            return true;
        }
        return false;
    }

    void reset() {
        startTime = millis();
        running = true;
    }

    void stop() {
        running = false;
    }

    bool active() const {
        return running;
    }
};