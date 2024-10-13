public class Main {
    public static void main(String[] args) {
        if (args.length != 3) {
            System.out.println("error in the arguments ");
            System.out.println("Example: java test add 10.5 5.5");
            return;
        }
        
        String operation = args[0];
        Double A, B;
        
        try {
            A = Double.parseDouble(args[1]);
            B = Double.parseDouble(args[2]);
        } catch (NumberFormatException e) {
            System.out.println("Error: A and B must be valid numbers.");
            return;
        }
        
        switch (operation.toLowerCase()) {
            case "+":
                Add addOperation = new Add();
                Double result = addOperation.compute(A, B);
                System.out.println("Result: " + result);
                break;
                case "-":
                Minus op = new Minus();
                result = op.compute(A, B);
                System.out.println("Result: " + result);
                break;
                case "/":
                Division op1 = new Division();
                result = op1.compute(A, B);
                System.out.println("Result: " + result);
                break;
                case "*":
                Multiplication op2 = new Multiplication();
                result = op2.compute(A, B);
                System.out.println("Result: " + result);
                break;      
                    default:
                System.out.println("Error: Unsupported operation. Only 'add' is supported.");
                break;
        }
    }
}
