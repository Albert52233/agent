public class fi {
    public static long fib(int n) {
        if (n < 0) {
            throw new IllegalArgumentException("n must be non-negative");
        }
        long a = 0, b = 1;
        for (int i = 0; i < n; i++) {
            long temp = a;
            a = b;
            b = temp + b;
        }
        return a;
    }

    public static void main(String[] args) {
        if (args.length != 1) {
            System.out.println("Usage: java fi <n>");
            System.exit(1);
        }
        try {
            int n = Integer.parseInt(args[0]);
            System.out.println(fib(n));
        } catch (NumberFormatException e) {
            System.out.println("Error: n must be an integer");
            System.exit(1);
        } catch (IllegalArgumentException e) {
            System.out.println("Error: " + e.getMessage());
            System.exit(1);
        }
    }
}
