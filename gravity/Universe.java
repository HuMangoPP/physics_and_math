import java.awt.*;
import java.awt.event.MouseEvent;
import java.util.HashSet;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import javax.swing.*;
import javax.swing.event.*;

public class Universe {
    GamePanel panel;
    JFrame frame;
    Sun sun;
    PlanetGroup planetGroup;
    UserInput input;
    
    static final int HEIGHT = 720;
    static final int WIDTH = 1280;
    static final int FRAME_DURATION = 5;
    static final double GRAVITY_CONSTANT = 5000;

    public static void main(String[] args) {
        Universe universe = new Universe();
        universe.start();
    }

    public void start() {
        sun = new Sun();
        planetGroup = new PlanetGroup();
        input = new UserInput();

        System.out.println("Press space to apply a radially outwards force");
        System.out.println("Press del to clear the planets");
        System.out.println("Press enter to spawn a new planet"); 

        this.panel = new GamePanel();
        this.panel.setBackground(Color.BLACK);
        this.panel.setOpaque(false);
        this.frame = new JFrame("Universe");
        this.frame.getContentPane().setBackground(Color.BLACK);
        this.frame.getContentPane().add(BorderLayout.CENTER, this.panel);
        this.frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        this.frame.setSize(WIDTH, HEIGHT);
        this.frame.setVisible(true);
        this.frame.setResizable(false);

        this.frame.addMouseListener(input);
        this.frame.addKeyListener(input);
        this.panel.addMouseListener(input);
        this.panel.addKeyListener(input);
    }

    class GamePanel extends JPanel {
        public void paintComponent(Graphics g) {
            sun.draw(g);
            planetGroup.draw(g);
            planetGroup.update(sun);
            try {
                Thread.sleep(FRAME_DURATION);
            } catch (InterruptedException e) {}
            frame.repaint();
        }
    }

    class Sun {
        int x, y, r;

        Sun() {
            x = WIDTH/2;
            y = HEIGHT/2;
            r = 25;
        }

        public void draw(Graphics g) {
            g.setColor(Color.YELLOW);
            g.fillOval(x-r, y-r, 2*r, 2*r);
        }
    }

    class Planet {
        double x, y;
        int r;
        double[] acc = new double[2];
        double[] vel = new double[2];
    
        Planet(int orbitR) {
            x = WIDTH/2;
            y = HEIGHT/2-orbitR;
            r = 10;
            double a = GRAVITY_CONSTANT/orbitR/orbitR;
            acc[0] = 0;
            acc[1] = a;
            vel[0] = Math.sqrt(a*orbitR);
            vel[1] = 0;
        }

        public void draw(Graphics g) {
            g.setColor(Color.RED);
            g.fillOval((int)x-r, (int)y-r, 2*r, 2*r);
            g.setColor(Color.BLUE);
            g.drawLine((int)x, (int)y, (int)(x+vel[0]*10), (int)(y+vel[1]*10)); //velocity vector
            g.setColor(Color.CYAN);
            g.drawLine((int)x, (int)y, (int)(x+acc[0]*500), (int)(y+acc[1]*500)); //acceleration vector
        }

        public void update(Sun sun) {
            double dx = 1.0*sun.x-x;
            double dy = 1.0*sun.y-y;
            double drSq = dx*dx+dy*dy;
            double a = GRAVITY_CONSTANT/drSq;

            acc[0] = a*dx/Math.sqrt(drSq);
            acc[1] = a*dy/Math.sqrt(drSq);

            vel[0]+=acc[0];
            vel[1]+=acc[1];

            x +=vel[0];
            y +=vel[1];
        }

        public void applyForce() {
            double dx = 1.0*sun.x-x;
            double dy = 1.0*sun.y-y;
            double drSq = dx*dx+dy*dy;
            double a = 2.5;
            acc[0] = -a*dx/Math.sqrt(drSq);
            acc[1] = -a*dy/Math.sqrt(drSq);

            vel[0]+=acc[0];
            vel[1]+=acc[1];

            x +=vel[0];
            y +=vel[1];
        }
    }

    class PlanetGroup {
        HashSet<Planet> planets = new HashSet<>();

        PlanetGroup() {
            planets.add(new Planet(200));
        }

        public void spawn() {
            planets.add(new Planet(200));
        }

        public void clear() {
            planets.clear();
        }

        public void update(Sun sun) {
            for (Planet planet: planets) {
                planet.update(sun);
            }
        }

        public void draw(Graphics g) {
            for (Planet planet: planets) {
                planet.draw(g);
            }
        }

        public void applyForce() {
            for (Planet planet: planets) {
                planet.applyForce();
            }
        }
    }

    class UserInput implements MouseInputListener, KeyListener{

        @Override
        public void mouseClicked(MouseEvent e) {
            // TODO Auto-generated method stub
            
        }

        @Override
        public void mousePressed(MouseEvent e) {
            // TODO Auto-generated method stub
            
        }

        @Override
        public void mouseReleased(MouseEvent e) {
            // TODO Auto-generated method stub
            planetGroup.applyForce();
        }

        @Override
        public void mouseEntered(MouseEvent e) {
            // TODO Auto-generated method stub
            
        }

        @Override
        public void mouseExited(MouseEvent e) {
            // TODO Auto-generated method stub
            
        }

        @Override
        public void mouseDragged(MouseEvent e) {
            // TODO Auto-generated method stub
            
        }

        @Override
        public void mouseMoved(MouseEvent e) {
            // TODO Auto-generated method stub
            
        }

        @Override
        public void keyTyped(KeyEvent e) {
            // TODO Auto-generated method stub
            
        }

        @Override
        public void keyPressed(KeyEvent e) {
            // TODO Auto-generated method stub
            if (e.getKeyCode()==KeyEvent.VK_D) {
                sun.x+=5;
            } else if (e.getKeyCode()==KeyEvent.VK_A) {
                sun.x-=5;
            }

            if (e.getKeyCode()==KeyEvent.VK_W) {
                sun.y-=5;
            } else if (e.getKeyCode()==KeyEvent.VK_S) {
                sun.y+=5;
            }

            if (e.getKeyCode()==KeyEvent.VK_DELETE) {
                planetGroup.clear();
            }
            if (e.getKeyCode()==KeyEvent.VK_ENTER) {
                planetGroup.spawn();
            }
        }

        @Override
        public void keyReleased(KeyEvent e) {
            // TODO Auto-generated method stub
            if (e.getKeyCode()==KeyEvent.VK_SPACE) {
                planetGroup.applyForce();
            }
        }
        
    }
}